import random
from os import path
import logging
import argparse
from inspect import ismodule, getmembers
import pandas as pd

import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display

import apps

logging.basicConfig(level=logging.INFO)

APPS = filter(lambda member: ismodule(member[1]), getmembers(apps))
DISPLAY = Display(visible=1, size=(1280, 720))
PROXIES_TABLE = pd.read_csv('proxy_list.csv', delimiter=';')

def play_url(in_url):
    proxy = PROXIES_TABLE.sample(1)
    proxy_host = proxy.sample(1).iloc[0]['host']
    proxy_port = proxy.sample(1).iloc[0]['port']
    fp = webdriver.FirefoxProfile()
    fp.set_preference('media.volume_scale', '0.0')
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.ssl", proxy_host)
    fp.set_preference("network.proxy.ssl_port", proxy_port)
    fp.set_preference("network.proxy.http", proxy_host)
    fp.set_preference("network.proxy.http_port", proxy_port)
    try:
        driver = webdriver.Firefox(
            executable_path=path.join(path.dirname(path.abspath(__file__)), 'geckodriver'),
            firefox_profile=fp
        )
        for app_name, app in APPS:
            if app.URL_PATTERN in in_url:
                app.play(in_url, driver)
                logging.info('Played on {}'.format(app_name))
    except Exception as e:
        logging.error('Exception using proxy {}:{}'.format(proxy_host, proxy_port))
    finally:
        driver.quit()
    


def play_plan(in_url, in_plays_number):
    global DISPLAY
    DISPLAY.start()
    for turn in xrange(in_plays_number):
        logging.info('{}/{}'.format(turn, in_plays_number))
        play_url(in_url)
        sleep_period = int(random.uniform(5, 15))
        time.sleep(sleep_period)
    DISPLAY.stop()


def build_argument_parser():
    result = argparse.ArgumentParser()
    result.add_argument('--url', required=True)
    result.add_argument('-n', required=True, type=int)
    return result


if __name__ == '__main__':
    parser = build_argument_parser()
    args = parser.parse_args()
    play_plan(args.url, args.n)
