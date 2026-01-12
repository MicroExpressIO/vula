# Example calling code using requests to interact with the Flask server

import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

# Supported search engines and their query URLs
SEARCH_ENGINES = {
    "google": "https://www.google.com/search?q={}",
    "bing": "https://www.bing.com/search?q={}",
    "duckduckgo": "https://duckduckgo.com/html/?q={}"
}
DEFAULT_ENGINE = "google"

def fetch_search_results(engine, keywords):
    if engine not in SEARCH_ENGINES:
        return None, f"Unsupported search engine: {engine}"
    url = SEARCH_ENGINES[engine].format(requests.utils.quote(keywords))
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        # Return raw HTML for simplicity; parsing can be added as needed
        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Extract visible text and links (simplified for Google/Bing/DuckDuckGo)
        results = []
        # For Google, results are in <div class="g">
        for result in soup.select("div.g"):
            title = result.find("h3")
            link = result.find("a", href=True)
            snippet = result.find("span", {"class": "aCOpRe"})
            if title and link:
                results.append({
                    "title": title.get_text(strip=True),
                    "link": link["href"],
                    "snippet": snippet.get_text(strip=True) if snippet else ""
                })
        # Fallback: If no results found, just return all text
        if not results:
            text = soup.get_text(separator="\n", strip=True)
            results = [{"text": text}]
        return results, None
    except Exception as e:
        return None, str(e)

@app.route('/search', methods=['POST'])
def search_default():
    data = request.get_json()
    keywords = data.get('keywords')
    if not keywords:
        return jsonify({"error": "Missing keywords"}), 400
    results, error = fetch_search_results(DEFAULT_ENGINE, keywords)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"results": results})

@app.route('/search_custom', methods=['POST'])
def search_custom():
    data = request.get_json()
    engine = data.get('engine', DEFAULT_ENGINE).lower()
    keywords = data.get('keywords')
    if not keywords:
        return jsonify({"error": "Missing keywords"}), 400
    results, error = fetch_search_results(engine, keywords)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
  