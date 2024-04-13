import requests
from app.dataclasses.scraper import Scraper


class ScraperManager:
    def __init__(self):
        self.scrapers = []

    def register(self, name: str, url: str) -> bool:
        obj = ScraperManager(name=name, url=url)
        try:
            self.scrapers.append(obj)
            print("Added scraper { 'name':'" + name + "', 'url':'" + url + "'}")
            return True
        except:
            print("Unable to add scraper { 'name':'" + name + "', 'url':'" + url + "'}")
            return False

    def run(self, url: str) -> tuple:
        for scraper in self.scrapers:
            try:
                result = requests.post(scraper.url, json={"url": url})
                if result.status_code == 400:
                    continue
                if result.status_code == 500:
                    print("Error calling " + scraper)
                    continue
                json = result.json()

                price, sep, appendix = json['price'].partition(" ")

                return json['name'].strip(), price.strip(), json['currency'].strip(), json['date_time']
            except Exception as e:
                print("Error calling scraper " + scraper)
                print(e)
                self.scrapers.remove(scraper)
        return "", "", "", ""
