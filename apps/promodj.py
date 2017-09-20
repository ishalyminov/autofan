import logging
import random
import time

logging.basicConfig(level=logging.INFO)

URL_PATTERN = 'promodj'


def play(in_url, in_driver):
    in_driver.get(in_url)
    time.sleep(5)
    in_driver\
        .find_element_by_css_selector('.playerr_bigplaybutton')\
        .click()
    # assuming it's enough time for a play to be registered
    sleep_period = int(random.uniform(60, 100))
    time.sleep(sleep_period)
