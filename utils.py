import requests
from bs4 import BeautifulSoup

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

def fetch_content(url, summary=False):
    """
    Fetches the content of the given URL.
    Returns a summary if the summary parameter is set to True.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            text = ' '.join(soup.stripped_strings)
            return text[:300] + '...' if summary else text[:3500]
        else:
            return None
    except Exception as e:
        print(f"Error fetching content: {e}")
        return None

def process_results(results):
    formatted_results = [SearchResult(res['title'], res['link']) for res in results]

    for result in formatted_results[:5]:
        result.summary = fetch_content(result.link, summary=True) or "Error fetching summary"

    for result in formatted_results[:1]:
        result.full_content = fetch_content(result.link, summary=False) or "Error fetching content"

    return [res.to_dict() for res in formatted_results][:5]
