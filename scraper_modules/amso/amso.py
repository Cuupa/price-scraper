import socket
import time
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests
import random
from flask import Flask, request, abort

hostnames = ["amso.eu"]
currencies = ["€"]

app = Flask(__name__)

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]


def is_responsible(url):
    hostname = urlsplit(url).hostname.replace("www.", "")
    return hostname in hostnames


@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        return _scrape(request.get_json())
    except Exception as e:
        print(e)
        return {"status": "error"}, 500


def _scrape(json):
    if len(json) == 0:
        abort(400)

    url = json['url']
    if not is_responsible(url):
        return {"status": "not-responsible"}, 400

    headers = {'User-Agent': random.choice(user_agents)}
    date_time = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"status": "error"}, 500

    soup = BeautifulSoup(response.content, 'html.parser')
    price = soup.find(id="projector_price_value").text.strip()
    name = soup.find(class_="product_name__name m-0").text.strip()

    if price is not None:
        sanitized = price.replace(",", ".").strip()
        currency = or_regex(currencies).search(sanitized).group(0)
        price = sanitized.replace("*", "").replace("€", "").strip()
        return {
            "status": "success",
            "name": name,
            "price": price,
            "currency": currency,
            "date_time": date_time
        }
    return {"status": "error"}, 500


def or_regex(symbols):
    return re.compile('|'.join(re.escape(s) for s in symbols))


def register(hostname: str, scraper_port: int):
    while True:
        time.sleep(5)
        try:
            response = requests.post("http://localhost:5000/api/scraper/register",
                                     json={"url": f"http://{hostname}:{scraper_port}/api/scrape",
                                           "name": hostnames[0]})
            if response.status_code == 200:
                print("Successfully registered scraper")
                break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    register(socket.gethostbyname(socket.gethostname()), port)
    app.run('0.0.0.0', port)
