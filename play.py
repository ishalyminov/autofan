import random
import logging
import argparse
from inspect import ismodule, getmembers
import time

import os
from selenium import webdriver

import apps
from proxy import get_proxy, get_seed_proxies

logging.basicConfig(level=logging.INFO)

APPS = filter(lambda member: ismodule(member[1]), getmembers(apps))
PROXIES = get_seed_proxies()


def play_url(in_url):
    global PROXIES
    try:
        proxy_host, proxy_port = get_proxy()
        PROXIES.add((proxy_host, proxy_port))
    except:
        logging.error('Failed to get proxy')
        proxy_host, proxy_port = random.choice(list(PROXIES))
    logging.info('using proxy: {}:{}'.format(proxy_host, proxy_port))

    try:
        driver = None
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            '--proxy-server={}:{}'.format(proxy_host, proxy_port)
        )
        chrome_options.add_argument('--headless')
        driver = \
            webdriver.Chrome(os.environ['CHROME_BINARY'], chrome_options=chrome_options) \
            if 'CHROME_BINARY' in os.environ \
            else webdriver.Chrome(chrome_options=chrome_options)
        for app_name, app in APPS:
            if app.URL_PATTERN in in_url:
                app.play(in_url, driver)
                logging.info('Played on {}'.format(app_name))
    except Exception as e:
        logging.error('Exception using proxy {}:{}'.format(proxy_host, proxy_port))
        PROXIES.remove((proxy_host, proxy_port))
        raise
    finally:
        if driver is not None:
            driver.quit()


def play_plan(in_url, in_plays_number):
    for turn in xrange(in_plays_number):
        logging.info('{}/{}'.format(turn, in_plays_number))
        play_url(in_url)
        sleep_period = int(random.uniform(5, 15))
        time.sleep(sleep_period)


def build_argument_parser():
    result = argparse.ArgumentParser()
    result.add_argument('--url', required=True)
    result.add_argument('-n', required=True, type=int)
    return result


if __name__ == '__main__':
    parser = build_argument_parser()
    args = parser.parse_args()
    play_plan(args.url, args.n)
