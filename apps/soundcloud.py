import logging
import time
import random

logging.basicConfig(level=logging.INFO)

URL_PATTERN = 'soundcloud'


def play(in_url, in_driver):
    in_driver.get(in_url)
    # assuming it's enough time for a play to be registered
    sleep_period = int(random.uniform(40, 60))
    time.sleep(sleep_period)

