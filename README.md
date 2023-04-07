# Google Search Plugin

A Flask app that uses the Google Custom Search API to search the web and fetch the inner text of the first link in the search results.

## Requirements

- Python 3.6+
- Flask
- Requests
- BeautifulSoup4
- LXML
- python-dotenv

## Installation (Heroku)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Sogody/google-chatgpt-plugin)
## Installation (Local)

1. Clone the repository:

```bash
git clone https://github.com/Sogody/google-chatgpt-plugin.git

cd google-search-plugin
```

Replace `yourusername` and `google-search-plugin` with your actual GitHub username and repository name.

2. Create a virtual environment and activate it:

- On Linux and macOS:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- On Windows:

  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Create a .env file in the project directory with the following content:

```makefile
GOOGLE_API_KEY=your_google_api_key
CUSTOM_SEARCH_ENGINE_ID=your_custom_search_engine_id
```

Replace your_google_api_key and your_custom_search_engine_id with your actual API key and custom search engine ID.

You can create your Google API KEY in https://console.cloud.google.com/apis/credentials.

You can get your custom search engine id in https://cse.google.com/cse/create/new.

## Usage

1. Run the Flask app:

```bash
python app.py

```

2. Access the app at http://localhost:5000/.

3. To search using the Google Custom Search API and fetch the inner text of the first link in the search results, send a GET request to the /search endpoint with the query parameter q:

```bash
http://localhost:5000/search?q=your_search_query
```

Replace your_search_query with your actual search query.

4. To access the OpenAPI specification and the logo, visit the following URLs:

OpenAPI specification: http://localhost:5000/.well-known/openapi.yaml
Logo: http://localhost:5000/.well-known/logo.png
Replace localhost:5000 with your actual app URL when you deploy it to a server.

## Deploy

Replace http://localhost:5000 with your actual app URL in OpenAPI specification and ai-plugin.json.

<a href="https://heroku.com/deploy?template=https://github.com/Sogody/google-chatgpt-plugin/tree/main">
  <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy">
</a>

## License

Please add information about the license you are using for your project (e.g., MIT License, Apache License, etc.).

