import requests
from bs4 import BeautifulSoup
import json
from transformers import GPT2Tokenizer
from indexer import vector_index

MAX_TOKENS = 2048

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

def fetch_content(url, summary=False, query='', vectorize=False):
    """
    Fetches the content of the given URL.
    Returns a summary if the summary parameter is set to True.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            text = ' '.join(soup.stripped_strings)
            text = text[:300] + '...' if summary else text
            if vectorize && check_token_count(text, MAX_TOKENS):
                text = vector_index(text, query, max_tokens = MAX_TOKENS)

            return text
        else:
            return None
    except Exception as e:
        print(f"Error fetching content: {e}")
        return None

def process_results(results, query, has_openai_key = None):
    formatted_results = [SearchResult(res['title'], res['link']) for res in results]

    for result in formatted_results[:5]:
        result.summary = fetch_content(
            result.link,
            summary=True,
            query=query,
            vectorize=has_openai_key
        ) or "Error fetching summary"

    for result in formatted_results[:3]:
        result.full_content = fetch_content(
            result.link, summary=False,
            query=query,
            vectorize=has_openai_key
        ) or "Error fetching content"

    return [res.to_dict() for res in formatted_results][:5]

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def check_token_count(results, max_tokens):
    results = json.dumps(results)
    tokenized_output = tokenizer.encode(results)
    token_count = len(tokenized_output)
    print(token_count)
    return token_count > max_tokens
