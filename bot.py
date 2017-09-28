import random

import os

from play import play_url


def main(in_playlist):
    while True:
        url = random.choice(in_playlist)
        play_url(url)


if __name__ == '__main__':
    playlist = os.environ['PLAYLIST'].split('\n')
    main(playlist)
