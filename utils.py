import os
from io import BytesIO
import requests
import openai
from bs4 import BeautifulSoup
from pypdf import PdfReader
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
    Fetches the text content of the given URL. If the URL is a PDF, it will extract the text from the PDF.
    """
    try:
        if debug:
            print(f"Fetching content for {url}")

        headers = {}
        headers['User-Agent'] = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        headers['Referer'] = f"https://www.google.com/"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '').lower()
            if 'application/pdf' in content_type or url.lower().endswith(".pdf"):
                with BytesIO(response.content) as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
            else:
                soup = BeautifulSoup(response.text, 'lxml')
                text = ' '.join(soup.stripped_strings)
            return text[:3500]
        else:
            return None
    except Exception as e:
        print(f"Error fetching content: {e}")
        return None

def summarize(text, query, model="text-davinci-003", tokens=500):
    prompt = f"Please summarize all the relevant information and if there is not any reply with only 'Nothing related found' in the following text based on the query: {query}\n###\n{text}"
    if debug:
        print(f"Summarizing query: Please summarize all the relevant information and if there is not any reply with only 'Nothing related found' in the following text based on the query: {query}")
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
