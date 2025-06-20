import time as _time
import toml as _toml
import os as _os

from src.network import send_post_request, is_url_valid
from src.event import subscribe as event_subscribe, unsubscribe as event_unsubscribe, post_event as event_post
from src.logger import logger as log, add_logging_level, Colorcode, create_logger
from src.email_listener import EmailListener
from src.multi_task import StoppableThread
from src.api_server import start as api_server_start
from src.discord_utilities import Embed as DiscordEmbed
from src.PlanToRun import run_at as plan_to_run_run_at, terminate as plan_to_run_terminate
from src.constants import TRADINGVIEW_ALERT_EMAIL_ADDRESS, RETRY_AFTER_HEADER, POST_REQUEST_HEADERS

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
    exit()
