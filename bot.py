import random

import os

import sys
import traceback

import time

from play import play_url


def main(in_playlist):
    while True:
        url = random.choice(in_playlist)
        try:
            play_url(url)
        except Exception as e:
            traceback.print_exc()
            print 'crashed on url: {}'.format(url)
        time.sleep(random.uniform(10, 30))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        playlist = os.environ['PLAYLIST'].split('\n')
    else:
        with open(sys.argv[1]) as playlist_in:
            playlist = filter(
                len,
                [line.strip() for line in playlist_in.readlines()]
            )
    main(playlist)
