import json
from os import path

CONFIG_FILE = path.join(path.dirname(__file__), 'config.json')
with open(CONFIG_FILE) as config_in:
    CONFIG = json.load(config_in)
