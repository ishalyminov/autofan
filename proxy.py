import requests
import json
from retrying import retry

from config import CONFIG


def get_seed_proxies(max_number=10):
    result = set([])
    while len(result) != max_number:
        try:
            proxy_host, proxy_port = get_proxy()
            result.add((proxy_host, proxy_port))
        except Exception as e:
            break
    return result


def get_proxy():
    proxy_configs = CONFIG['proxy_config']
    for api_name, api_config in proxy_configs.iteritems():
        try:
            proxy_host, proxy_port = call_proxy_api(api_config)
            return proxy_host, proxy_port
        except Exception as e:
            continue
    raise 'Could\'t not get a proxy'


@retry(wait_random_min=1000, wait_random_max=2000, stop_max_attempt_number=3)
def call_proxy_api(in_proxy_config):
    api_response = requests.get(
        in_proxy_config['api_url'],
        params=in_proxy_config['params']
    )
    if api_response.status_code != 200:
        raise 'Unable to get a proxy server'
    content = json.loads(api_response.content)
    return (
        content[in_proxy_config['response_fields']['ip']],
        content[in_proxy_config['response_fields']['port']]
    )

