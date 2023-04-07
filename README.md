# Google Search Plugin

A Flask app that uses the Google Custom Search API to search the web and fetch the summary for five first links in the search results as well as inner text of the first three links. The purpose of this app is to be used as a plugin for ChatGPT. 

## How it works

https://user-images.githubusercontent.com/1191646/230582839-966d8695-4791-4a6c-9806-24303583afbd.mp4


## Requirements

- Python 3.6+
- Flask
- Requests
- BeautifulSoup4
- LXML
- python-dotenv

## Installation (Heroku)

Deploy to Heroku with one click by clicking the button below: 

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Sogody/google-chatgpt-plugin)

**A Google API Key and a Custom Search Engine ID is required to complete the installation, both of which can be generated [here](https://console.cloud.google.com/apis/credentials) and [here](https://cse.google.com/cse/create/new).**

Once the installation is complete, grab the APP URL and add it to ChatGPT Plugin installation page. To do this, click the "View" button at the bottom of the page, and copy the URL from the address bar.

## Installation (Local)

1. Clone the repository:

```bash
git clone https://github.com/Sogody/google-chatgpt-plugin.git

cd google-search-plugin
```

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

Replace `your_google_api_key` and `your_custom_search_engine_id` with your actual API key and custom search engine ID.

You can create your Google API KEY in https://console.cloud.google.com/apis/credentials.

You can get your custom search engine id in https://cse.google.com/cse/create/new.

## Usage

1. Run the Flask app:

```bash
python main.py
```

2. Access the app at http://localhost:5000/.

3. To search using the Google Custom Search API and fetch the inner text of the first link in the search results, send a GET request to the /search endpoint with the query parameter q:

```bash
http://localhost:5000/search?q=your_search_query
```

Replace your_search_query with your actual search query.

## Deploy

For compatibility with ChatGPT, deploy the plugin on a publicly accessible host. Deployment steps vary depending on the platform, however, at the end, you need to enter the domain name (and possibly port if deploying to a non-standard port) at ChatGPT Plugin installation page.

## License
MIT
