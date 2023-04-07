from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os
from utils import process_results

app = Flask(__name__)
CORS(app)

def load_environment_variables():
    load_dotenv()
    return os.environ.get("GOOGLE_API_KEY"), os.environ.get("CUSTOM_SEARCH_ENGINE_ID")

API_KEY, CX = load_environment_variables()

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
        formatted_results = process_results(results)
        return jsonify({"results": formatted_results})
    else:
        return jsonify({"error": "Error fetching search results"}), response.status_code

@app.route('/.well-known/<path:filename>')
def serve_well_known_files(filename):
    return send_from_directory(os.path.join(os.getcwd(), ".well-known"), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
