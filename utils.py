import datetime
import os
from io import BytesIO
import unicodedata
import requests
import openai
from bs4 import BeautifulSoup
from pypdf import PdfReader
import tiktoken
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI API client
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.organization = os.environ.get("OPENAI_ORGANIZATION_ID")

# Initialize tiktoken Tokenizer
encoding = tiktoken.get_encoding("cl100k_base")

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
    Not meant for code snippets as we strip out all the HTML tags and most whitespace chacters.
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
                soup = BeautifulSoup(response.text, 'html.parser')
                text = unicodedata.normalize('NFC', u' '.join(soup.body.stripped_strings))
            return text
        else:
            return None
    except Exception as e:
        print(f"Error fetching content: {e}")
        return None

def summarize(text, query, model="text-davinci-003", max_tokens=500):
    prompt = f"The current date and time is {datetime.datetime.now()}. Please summarize all the relevant information and if there is not any reply with only 'Nothing related found' in the following text based on the query: {query}\n###\n{text}"
    prompt = text_shorten(prompt, 3500) + "\n###\n"
    if debug:
        print(f"Summarizing query: The current date and time is {datetime.datetime.now()}. Please summarize all the relevant information and if there is not any reply with only 'Nothing related found' in the following text based on the query: {query}")
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def text_shorten(text, max_tokens=2000):
    tokens = encoding.encode(text)
    if len(tokens) < max_tokens:
        return text
    else:
        shortened_tokens = tokens[:max_tokens]
        shortened_text = encoding.decode(shortened_tokens)
        return shortened_text

def process_results(results, query):
    formatted_results = [SearchResult(res['title'], res['link']) for res in results]

    for i, result in enumerate(formatted_results):
        result.full_content = fetch_content(result.link) or "Error fetching content"
        result.summary = None

        if i < 3:
            result.full_content = text_shorten(result.full_content, 1000)

    for result in formatted_results[3:]:
        if debug:
            print(f"Summarizing content for {result.title} {result.link}")
        result.summary = summarize(result.full_content, query, max_tokens=250) or "Error fetching summary"
        result.full_content = None

    return [res.to_dict() for res in formatted_results]
