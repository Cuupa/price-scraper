import os
import socket
import time
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests
import random
from flask import Flask, request, abort

hostnames = ["www.yournextit.de", "yournextit.de"]
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
        return {
            "status": "error"
        }, 500
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        prices = soup.find_all(class_="product-detail-price")
        name = soup.find(class_="product-detail-name").text.strip()

        if len(prices) > 0:
            sanitized = prices[0].text.replace(",", ".").strip()
            currency = or_regex(currencies).search(sanitized).group(0)
            price = sanitized.replace("*", "").replace(currency, "").strip()
            return {
                "status": "success",
                "name": name,
                "price": price,
                "currency": currency,
                "date_time": date_time
            }


def or_regex(symbols):
    return re.compile('|'.join(re.escape(s) for s in symbols))


def register(local_hostname: str, local_port: int, app_address: str, app_port: str):
    while True:
        time.sleep(5)
        print(f"Trying to connect to http://{app_address}:{app_port}/api/scraper/register")
        try:
            response = requests.post(f"http://{app_address}:{app_port}/api/scraper/register",
                                     json={"url": f"http://{local_hostname}:{str(local_port)}/api/scrape",
                                           "name": hostnames[0]})
            if response.status_code == 200:
                print("Successfully registered scraper")
                break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 0))
    local_port = sock.getsockname()[1]
    local_hostname = socket.gethostbyname(socket.gethostname())
    sock.close()

    app_address = os.environ.get("HOST_URL", "localhost")
    app_port = os.environ.get("HOST_PORT", "5000")

    register(local_hostname, local_port, app_address, app_port)
    app.run('0.0.0.0', local_port)
