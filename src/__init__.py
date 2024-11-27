import time as _time
from .smart_import import try_import

try_import("toml")
import toml as _toml
import os as _os

from .network import send_post_request, is_url_valid
from .event import subscribe as event_subscribe, unsubscribe as event_unsubscribe, post_event as event_post
from .logger import logger as log, add_logging_level, Colorcode, create_logger
from .http_status import http_status
from .email_listener import EmailListener
from .multi_task import StoppableThread
from .api_server import start as api_server_start
from .discord_utilities import Embed as DiscordEmbed
from .PlanToRun import run_at as plan_to_run_run_at, terminate as plan_to_run_terminate
from .constants import TRADINGVIEW_ALERT_EMAIL_ADDRESS, RETRY_AFTER_HEADER

class log_levels:
    """
    Log-Levels:\n
        DEBUG    = 10\n
        INFO     = 20\n
            OK        = 21\n
            DB        = 22\n
            DB_OK     = 23\n
        WARNING  = 30\n
        ERROR    = 40\n
            DB_ERROR = 41\n
        CRITICAL = 50\n
    """
    DEBUG = 10
    INFO = 20
    OK = 21
    # DB = 22
    # DB_OK = 23
    WARNING = 30
    ERROR = 40
    # DB_ERROR = 41
    CRITICAL = 50

__location__ = _os.path.realpath(_os.path.join(_os.getcwd(), _os.path.dirname(__file__))) # get current directory
project_main_directory = _os.path.dirname(__location__)

config = _toml.load(_os.path.join(project_main_directory, "config.toml"))

def shutdown(seconds:float = 10):
    """
    ### Description ###
    Shutdown the program after a certain amount of time in seconds.
    
    ### Parameters ###
        - `seconds` (float): The amount of time to wait before shutting down the program
    """
    log.warning(f"The program will shut down after {seconds}s...")
    _time.sleep(seconds)
    log.thread.stop()
    exit()


_webhook_urls = config.get("webhook_urls")
_proxy_url = config.get("proxy_url")
_proxies = {
    "http": _proxy_url,
    "https": _proxy_url
} if _proxy_url else None

# Validate proxy URL
if _proxies != None:
    if is_valid_url := is_url_valid(_proxy_url):
        log.info(f"Using proxy: {_proxy_url}")
    else:
        log.error(f"Invalid proxy URL: {_proxy_url}")
        exit()

def send_webhook(payload:str | dict):
    """
    ### Description ###
    Send a webhook to the specified URL(s).
    
    ### Parameters ###
        - `payload` (str | dict): The content of the webhook to send
        
    ### Example ###
    ```python
    send_webhook("Hello, World!")
    ```
    """
    headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
    for webhook_url in _webhook_urls:
        res = send_post_request(webhook_url, payload, headers, proxies=_proxies)
        if res.status_code >= 200 and res.status_code < 300:
            log.ok(f"Sent webhook to {webhook_url} successfully, response code: {res.status_code}")
        elif retry_after := res.headers.get("Retry-After"):
            if res.status_code == 429:
                log.warning(f"Sent webhook to {webhook_url} failed, response code: {res.status_code}, Content: {payload}, Retry-After header({RETRY_AFTER_HEADER}) found, auto retry after {retry_after}s...")
                plan_to_run_run_at(_time.time() + float(retry_after), send_webhook, payload)
                continue
            log.error(f"Sent webhook to {webhook_url} failed, response code: {res.status_code}, Content: {payload}.")
