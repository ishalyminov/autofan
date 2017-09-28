import argparse
import random

from play import play_url


def build_argument_parser():
    result = argparse.ArgumentParser()
    result.add_argument('--playlist', required=True)
    return result


def main(in_playlist_file):
    with open(in_playlist_file) as playlist_in:
        playlist = map(lambda x: x.strip(), playlist_in)
    while True:
        url = random.choice(playlist)
        play_url(playlist)


if __name__ == '__main__':
    parser = build_argument_parser()
    args = parser.parse_args()

    main(args.playlist)
