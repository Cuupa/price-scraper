import threading

import schedule
import time

from app.product_persistence import store
from app import scraper
from app.notifications import notifications

job: threading.Event
interval: int


def scrape_products():
    for product in store.all_products():
        try:
            (name, price, currency, date_time) = scraper.run(product.url)
            if name == "" or name is None:
                continue
            store.add_point(product.id, name, price, currency, date_time)
            if price < product.current_price and product.current_price is not None:
                notifications.notify(product, price)
        except Exception as error:
            print("An Error occured", error)


def run_continuously(interval=1) -> threading.Event:
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


background_job = run_continuously()


def run(job_interval=10):
    global interval
    interval = job_interval
    schedule.every(interval).minutes.do(scrape_products)
    global job
    job = run_continuously()


def update_settings(job_interval: int):
    job.set()
    run(job_interval)
