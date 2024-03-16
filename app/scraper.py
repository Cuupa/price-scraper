import requests
from app.dataclasses.scraper import Scraper

scrapers = []


def register(name: str, url: str) -> bool:
    obj = Scraper(name=name, url=url)
    try:
        scrapers.append(obj)
        print("Added scraper { 'name':'" + name + "', 'url':'" + url + "'}")
        return True
    except:
        print("Unable to add scraper { 'name':'" + name + "', 'url':'" + url + "'}")
        return False


def run(url: str) -> tuple:
    for scraper in scrapers:
        try:
            result = requests.post(scraper.url, json={"url": url})
            if result.status_code == 400:
                continue
            if result.status_code == 500:
                print("Error calling " + scraper)
                continue
            json = result.json()

            return json['name'], json['price'], json['currency'], json['date_time']
        except Exception as e:
            print("Error calling scraper " + scraper)
            print(e)
            scrapers.remove(scraper)
    return "", "", "", ""
