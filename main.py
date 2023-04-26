from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os
import json
import yaml
from utils import process_results

app = Flask(__name__)
CORS(app)

def load_environment_variables():
    load_dotenv()
    return \
        os.environ.get("GOOGLE_API_KEY"), \
        os.environ.get("CUSTOM_SEARCH_ENGINE_ID"), \
        os.environ.get("OPENAI_API_KEY")

API_KEY, CX, OPENAI_API_KEY = load_environment_variables()
has_openai_key = OPENAI_API_KEY != None

@app.route('/.well-known/ai-plugin.json', methods=['GET'])
def get_plugin_info():
    with open('.well-known/ai-plugin.json') as f:
        data = json.load(f)
        data['api']['url'] = f"{request.scheme}://{request.host}/.well-known/openapi.yaml"
        data['logo_url'] = f"{request.scheme}://{request.host}/.well-known/icon.png"

        return jsonify(data)

@app.route('/.well-known/openapi.yaml', methods=['GET'])
def get_openai_info():
    with open('.well-known/openapi.yaml') as f:
        data = yaml.safe_load(f)
        data['servers'][0]['url'] = f"{request.scheme}://{request.host}"
        yaml_data = yaml.dump(data)

        return Response(yaml_data, content_type='application/x-yaml')

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
        formatted_results = process_results(results, query, has_openai_key)

        return jsonify({"results": formatted_results})
    else:
        return jsonify({"error": "Error fetching search results"}), response.status_code

@app.route('/.well-known/<path:filename>')
def serve_well_known_files(filename):
    return send_from_directory(os.path.join(os.getcwd(), ".well-known"), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
