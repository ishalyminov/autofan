import requests
import json
from retrying import retry

PROXY_API_URL = 'https://api.proxicity.io/v2/proxy' 


@retry(wait_random_min=1000, wait_random_max=2000, stop_max_attempt_number=3)
def get_proxy(params={
    'protocol': 'http',
    'httpsSupport': 'true',
    'isAnonymous': 'true'
}):
    api_response = requests.get(PROXY_API_URL, params=params)
    if api_response.status_code != 200:
        raise 'Unable to get a proxy server'
    content = json.loads(api_response.content)
    return content['ipAddress'], content['port']

