import os
from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

API_KEY = ""
CX = ""

def fetch_inner_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            text = ' '.join(soup.stripped_strings)
            return text
        else:
            return None
    except Exception as e:
        print(f"Error fetching inner text: {e}")
        return None

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={query}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('items', [])
        formatted_results = [{'title': res['title'], 'link': res['link']} for res in results]

        # Fetch inner text of the first link
        first_link = formatted_results[0]['link'] if formatted_results else ''
        inner_text = fetch_inner_text(first_link)
        if inner_text:
            return jsonify({"results": formatted_results, "first_link_inner_text": inner_text})
        else:
            return jsonify({"results": formatted_results, "first_link_inner_text": "Error fetching inner text"})
    else:
        return jsonify({"error": "Error fetching search results"}), response.status_code

@app.route('/.well-known/<path:filename>')
def serve_well_known_files(filename):
    return send_from_directory(os.path.join(os.getcwd(), ".well-known"), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
