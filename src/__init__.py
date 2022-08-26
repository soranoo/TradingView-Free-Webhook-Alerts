import toml as _toml
import os as _os


from .logger import log, add_logging_level, Colorcode
from .http_status import http_status
from .email_listener import EmailListener

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