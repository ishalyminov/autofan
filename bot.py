import random

import os

from play import play_url


def main(in_playlist):
    while True:
        url = random.choice(in_playlist)
        try:
            play_url(url)
        except:
            print 'crashed on url: {}'.format(url)


if __name__ == '__main__':
    playlist = os.environ['PLAYLIST'].split('\n')
    main(playlist)
