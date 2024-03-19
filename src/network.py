import contextlib
import re
import json
import requests
from requests.adapters import HTTPAdapter, Retry

#! The "URL_REGEX" not support localhost use 127.0.0.1 instead
URL_REGEX = r"^https?:\/\/((?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$"
POST_REQUEST_HEADERS = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }

# increase retries number
requests.adapters.DEFAULT_RETRIES = 5

def is_url_valid(url:str) -> bool:
    """
    ### Description ###
    Check if the URL is valid

    ### Parameters ###
        - `url` (str): URL

    ### Returns ###
        - (bool): True if the URL is valid, False otherwise 
    """
    return isinstance(extract_url_domain(url), str)

def extract_url_domain(url:str) -> bool or str:
    """
    ### Description ###
    Extract domain from URL

    ### Parameters ###
        - `url` (str): URL

    ### Returns ###
        - (bool or str): False if the URL is invalid, domain if the URL is valid
    """
    return m[1] if (m := re.search(URL_REGEX, url)) else None

def send_post_request(url:str, payload:str or dict, headers:dict = None, proxies:dict = None) -> requests.models.Response:
    """
    ### Description ###
    Send HTTP POST request

    ### Parameters ###
        - `url` (str): URL
        - `payload` (str or dict): Payload
        - `headers` (dict): Headers
        - `proxies` (dict): Proxies

    ### Returns ###
        - (requests.models.Response): Response
    """
    if not is_url_valid(url):
        raise ValueError(f"Invalid URL <{url}>")
    # decode JSON if the payload is in JSON format
    with contextlib.suppress(Exception):
        payload = json.loads(payload)
    # convert to JSON
    payload = json.dumps(payload)
    # start a session
    session = requests.Session()
    # set retry policy
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    # add adapter to session
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session.post(
        url,
        data=payload,
        headers=POST_REQUEST_HEADERS if headers is None else headers,
        proxies=proxies
    )