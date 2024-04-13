import threading

import schedule
import time

from app import store
from app.notifications import notifications


class Scheduler:

    def __init__(self, scraper_manager):
        self.scraper_manager = scraper_manager
        self.job = threading.Event()
        self.interval = 0

    def scrape_products(self):
        for product in store.all_products():
            try:
                (name, price, currency, date_time) = self.scraper_manager.run(product.url)
                if name == "" or name is None:
                    continue
                store.add_point(product.id, name, price, currency, date_time)
                if product.current_price is not None and price < product.current_price:
                    notifications.notify(product, price)
            except Exception as error:
                print("An Error occured", error)

    def run_continuously(self, interval=1) -> threading.Event:
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run

    def run(self, job_interval=10):
        self.interval = job_interval
        schedule.every(self.interval).minutes.do(self.scrape_products)
        self.job = self.run_continuously()

    def update_settings(self, job_interval: int):
        self.job.set()
        self.run(job_interval)
