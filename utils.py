import os
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI API client
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.organization = os.environ.get("OPENAI_ORGANIZATION_ID")

debug = os.environ.get("DEBUG", False)

class SearchResult:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.summary = None
        self.full_content = None

    def to_dict(self):
        return {
            'title': self.title,
            'link': self.link,
            'summary': self.summary,
            'full_content': self.full_content
        }

def fetch_content(url):
    """
    Fetches the content of the given URL.
    """
    try:
        if debug:
            print(f"Fetching content for {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            text = ' '.join(soup.stripped_strings)
            return text[:3500]
        else:
            return None
    except Exception as e:
        print(f"Error fetching content: {e}")
        return None

def summarize(text, query, model="text-davinci-003", tokens=500):
    prompt = f"Please summarize all the relevant information in the following text based on the query: {query}\n###\n{text}"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def process_results(results, query):
    formatted_results = [SearchResult(res['title'], res['link']) for res in results]

    for result in formatted_results:
        if debug:
            print(f"Fetching content for {result.title} - {result.link}")
        result.full_content = fetch_content(result.link) or "Error fetching content"
        result.summary = None

    for result in formatted_results[3:]:
        if debug:
            print(f"Summarizing content for {result.title} - {result.link}")
        result.summary = summarize(result.full_content, query, tokens=250) or "Error fetching summary"
        result.full_content = None

    return [res.to_dict() for res in formatted_results]
