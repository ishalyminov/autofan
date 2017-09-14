import random
from os import path
import logging
import argparse
from inspect import ismodule, getmembers

import time
from selenium import webdriver

import apps
from proxy import get_proxy

logging.basicConfig(level=logging.INFO)

APPS = filter(lambda member: ismodule(member[1]), getmembers(apps))


def play_url(in_url):
    proxy_host, proxy_port = get_proxy()
    service_args = [
        '--proxy={}:{}'.format(proxy_host, proxy_port),
        '--proxy-type=https',
    ]
    try:
        driver = None
        driver = webdriver.PhantomJS(
            executable_path=path.join(path.dirname(__file__),
                                      'node_modules/.bin/phantomjs'),
            service_args=service_args
        )
        driver.set_window_size(1280, 720)
        for app_name, app in APPS:
            if app.URL_PATTERN in in_url:
                app.play(in_url, driver)
                logging.info('Played on {}'.format(app_name))
    except Exception as e:
        logging.error('Exception using proxy {}:{}'.format(proxy_host, proxy_port))
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