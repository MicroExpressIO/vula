
import requests
from flask import Flask, request, jsonify
'''
# Example 1: Search using the default engine (Google)
response = requests.post(
    "http://127.0.0.1:5000/search",
    json={"keywords": "python flask tutorial"}
)
print("Default search response:", response.json())

# Example 2: Search using a custom engine (Bing)
response = requests.post(
    "http://127.0.0.1:5000/search_custom",
    json={"engine": "bing", "keywords": "CVE-2024-36971"}
)
print("Custom search response (Bing):", response.json())
'''
'''
# Example 3: Search using a custom engine (DuckDuckGo)
response = requests.post(
    "http://127.0.0.1:5000/search_custom",
    json={"engine": "duckduckgo", "keywords": "CVE-2024-36971"}
)
print("Custom search response (DuckDuckGo):", response.json())
'''

from bs4 import BeautifulSoup

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def google(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)

    soup = BeautifulSoup(r.text, "html.parser")
    output = []
    for searchWrapper in soup.find_all('h3', {'class':'r'}): #this line may change in future based on google's web page structure
        url = searchWrapper.find('a')["href"] 
        text = searchWrapper.find('a').text.strip()
        result = {'text': text, 'url': url}
        output.append(result)

    return output

def run():    
    q="CVE-2024-36971"
    ret=google(q)
    print(f" response: \n\n {ret}")
    
if __name__ == '__main__':
    run()