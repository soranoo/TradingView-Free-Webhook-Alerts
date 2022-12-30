try:
    # If running with the current directory
    from smart_import import try_import
except ModuleNotFoundError or ImportError:
    # If running by parent directory
    from .smart_import import try_import

try_import("colorama")
try_import("colorlog")

import os
import logging
import colorama
from colorlog import ColoredFormatter

from datetime import datetime

class Colorcode:
    RESET = "\x1b[0m"
    BOLD = "\x1b[1m"
    DIM = "\x1b[2m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN = "\x1b[36m"
    WHITE = "\x1b[37m"
    GRAY = "\x1b[90m"

def find_project_directory() -> str:
    """
    ### Description ###
    Find the directory of the project.
    
    ### Returns ###
        - (str): The directory of the project.
    """
    THIS_DIRECTORY = project_dir = os.path.dirname(__file__)
    if __name__ == "__main__":
        return THIS_DIRECTORY
    import_abs_path = __name__.split(".")[:-1][::-1]
    for folder_name in import_abs_path:
        p_dir = project_dir.split(os.sep)
        if p_dir[-1] == folder_name:
            project_dir = os.path.dirname(project_dir)
        else:
            Warning(f"Cannot find the project directory, the logger will use <{THIS_DIRECTORY}> as the project directory")
            project_dir = THIS_DIRECTORY
            break
    return project_dir

def create_log_file_name() -> str:
    """
    ### Description ###
    Create the log file name.
    
    ### Returns ###
        - (str): The log file name with extension. EG. "23-12-2022.log"
    """
    DATE_FORMAT = "%d-%m-%Y"
    return f"{datetime.now().strftime(DATE_FORMAT)}.log"

def add_logging_level(level_name:str, level_number:int, log_color:str, method_name:str = None):
    """
    ### Description ###
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class. 
    
    - Reference: https://stackoverflow.com/a/35804945

    ### Parameters ###
        - `level_name` (str): Level name, normally is in all caps, eg. "DEBUG".
        - `level_number` (int): A numeric value that indicates the severity of a log message.
                                For example, `logging.DEBUG` is 10, `logging.INFO` is 20
                                and `logging.ERROR` is 40.
        - `log_color` (str): The color of that level log message.
        - `method_name` (str | optional): The name of the method that will be added to the logger class.
                                The name normally is in all lower case, eg. "debug".
                                If not specified, the `level_name` after lowercasing will be used.
    """
    
    method_name = method_name or level_name.lower()

    # validation
    if hasattr(logging, level_name):
       raise AttributeError(f"{level_name} already defined in logging module")
    elif hasattr(logging, method_name):
       raise AttributeError(f"{method_name} already defined in logging module")
    elif hasattr(logging.getLoggerClass(), method_name):
       raise AttributeError(f"{method_name} already defined in logger class")

    log_colors.update({level_name: log_color})

    # This method was inspired by the answers to Stack Overflow post
    # credit: http://stackoverflow.com/q/2183233/2988730, especially
    # credit: http://stackoverflow.com/a/13638084/2988730
    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(level_number):
            self._log(level_number, message, args, **kwargs)

    def log_to_root(message, *args, **kwargs):
        logging.log(level_number, message, *args, **kwargs)

    # register the new logging level
    logging.addLevelName(level_number, level_name)
    setattr(logging, level_name, level_number)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)


def get_datetime_formant(included_timezone:bool = False, 
                         use_local_version_time:bool = False,) -> str:
    """
    ### Description ###
    Get the datetime format.
    
    ### Parameters ###
    - `included_timezone` (bool | optional): Whether to include the timezone when logging.
        - `use_local_version_time` (bool | optional): Whether to use the local version of time.
                                                        EG. "Fri Dec 23 00:03:37 2022" instead of "23-12-2022 00:03:37"
    
    ### Returns ###
        - (str): The datetime format.
    """
    DATETIME_FORMAT = "%c" if use_local_version_time else "%d-%m-%Y %H:%M:%S"
    DATETIME_FORMAT_WITH_TIMEZONE = f"{DATETIME_FORMAT} %z"
    return DATETIME_FORMAT_WITH_TIMEZONE if included_timezone else DATETIME_FORMAT


def create_file_handler(log_folder_path:str = None, log_file_name:str = None,
                        included_timezone:bool = False, 
                        use_local_version_time:bool = False,) -> logging.FileHandler:
    """
    ### Description ###
    Create a file handler for the logger.
    
    ### Parameters ###
        - `log_folder_path` (str | optional): The path to the folder where the log file will be saved.
                                                If not specified, the log file will be saved in the project directory.
        - `log_file_name` (str | optional): The name of the log file.
                                            If not specified, the log file name will be the current date.
        - `included_timezone` (bool | optional): Whether to include the timezone when logging.
        - `use_local_version_time` (bool | optional): Whether to use the local version of time.
                                                        EG. "Fri Dec 23 00:03:37 2022" instead of "23-12-2022 00:03:37"
    
    ### Returns ###
        - (logging.FileHandler): The file handler.
    """
    log_folder_path = log_folder_path or os.path.join(find_project_directory(), "logs")
    log_file_name = log_file_name or create_log_file_name()
    date_format = get_datetime_formant(included_timezone, use_local_version_time)
    file_formatter = logging.Formatter("%(asctime)s | %(levelname)-9s | %(message)s", datefmt=date_format)
    
    # create new folder if not exist
    if log_folder_path and not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
        
    file_handler = logging.FileHandler(os.path.join(log_folder_path, log_file_name), "a", "utf-8")
    file_handler.setFormatter(file_formatter)
    return file_handler


def create_console_handler(color_print:bool = True, print_log_msg_color:bool = True,
                            included_timezone:bool = False, use_local_version_time:bool = False,) -> logging.FileHandler:
    """
    ### Description ###
    Create a file handler for the logger.
    
    - Reference: https://github.com/borntyping/python-colorlog
    - Reference: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    
    ### Parameters ###
        - `color_print` (bool | optional): Whether to print the log into the console with colors.
                                            If ture, the level name will be colored.
        - `print_log_msg_color` (bool | optional): Whether to print the log message with colors.
                                                    Requires `color_print` to be `True`.
        - `included_timezone` (bool | optional): Whether to include the timezone when logging.
        - `use_local_version_time` (bool | optional): Whether to use the local version of time.
                                                        EG. "Fri Dec 23 00:03:37 2022" instead of "23-12-2022 00:03:37"
    
    ### Returns ###
        - (logging.FileHandler): The file handler.
    """
    date_format = get_datetime_formant(included_timezone, use_local_version_time)
    
    console_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-9s | %(message)s", datefmt=date_format)
    console_color_formatter = ColoredFormatter(
        f"{Colorcode.GRAY}%(asctime)s{Colorcode.RESET} | %(log_color)s%(levelname)-9s%(reset)s | {'%(log_color)s' if print_log_msg_color else Colorcode.WHITE}%(message)s{Colorcode.RESET}",
        datefmt = date_format,
        log_colors = log_colors,
    )
    
    console_handler = logging.StreamHandler()
    if color_print:
        console_handler.setFormatter(console_color_formatter)
    else:
        console_handler.setFormatter(console_formatter)
    return console_handler


def create_logger(log_folder_path:str = None, save_log:bool = True,
                  color_print:bool = True, print_log_msg_color:bool = True, 
                  included_timezone:bool = False,use_local_version_time:bool = False,
                  log_level:int = logging.DEBUG, logger_name:str = "cofree", 
                  rebuild_mode:bool = False, rebuild_logger:logging.Logger = None) -> logging.Logger:
    """
    ### Description ###
    Create a logger.
    
    ### Parameters ###
        - `log_folder_path` (str | optional): The path to the folder where the log file will be saved.
                                                If not specified, the log file will be saved in the project directory.
        - `save_log` (bool | optional): Whether to save the log to a file.
        - `color_print` (bool | optional): Whether to print the log into the console with colors.
                                            If ture, the level name will be colored.
        - `print_log_msg_color` (bool | optional): Whether to print the log message with colors.
                                                    Requires `color_print` to be `True`.
        - `included_timezone` (bool | optional): Whether to include the timezone when logging.
        - `use_local_version_time` (bool | optional): Whether to use the local version of time.
                                                        EG. "Fri Dec 23 00:03:37 2022" instead of "23-12-2022 00:03:37"
        - `log_level` (int | optional): The level of the logger. Default is `logging.DEBUG`.
        - `logger_name` (str | optional): The name of the logger. Default is "cofree". 
                                            If `rebuild_mode` is `True`, this parameter will be ignored.
        
        - `rebuild_mode` (bool | optional): If `True`, no logger will be created and the new setting of
                                            file handler and console handler will be apply to `rebuild_logger`.
        - `rebuild_logger` (logging.Logger | optional): The logger to rebuild. Required if `rebuild_mode` is `True`.
    
    ### Returns ###
        - (logging.Logger): Logger object.
    """
    # Handler Example:
    # class MyLogHandler(logging.Handler):
    #     def emit(self, record):
    #         # Call the callback function when a log record is emitted
    #         print("Log record emitted:", record.msg)
    
    global logger_file_handler, logger_console_handler
    
    # catch python warning message
    logging.captureWarnings(True)
    
    if not rebuild_mode:
        # Create a logger
        logger = logging.getLogger(logger_name)
    else:
        if not rebuild_logger:
            raise ValueError("'rebuild_logger' is required if 'rebuild_mode' is True.")
        logger = rebuild_logger
        # remove old console handler and file handler
        if logger_console_handler:
            logger.removeHandler(logger_console_handler)
        if logger_file_handler:
            logger.removeHandler(logger_file_handler)

    logger.setLevel(level=log_level)
    
	# setup handlers
    logger_console_handler = create_console_handler(
        color_print = color_print, 
        print_log_msg_color = print_log_msg_color,
        included_timezone = included_timezone,
        use_local_version_time = use_local_version_time,
    )
    logger.addHandler(logger_console_handler)
    if save_log:
        logger_file_handler = create_file_handler(
            log_folder_path = log_folder_path, 
            log_file_name = create_log_file_name(),
            included_timezone = included_timezone,
            use_local_version_time = use_local_version_time
        )
        logger.addHandler(logger_file_handler)
        logger.debug(f"The log file will be saved in <{os.path.dirname(logger_file_handler.baseFilename)}>.")
    else:
        logger_file_handler = None
    
    return logger

# ---------------* initialization *---------------

#ref: https://shian420.pixnet.net/blog/post/350291572-%5Bpython%5D-logging-%E5%B9%AB%E4%BD%A0%E7%B4%80%E9%8C%84%E4%BB%BB%E4%BD%95%E8%A8%8A%E6%81%AF
#ref: https://titangene.github.io/article/python-logging.html
#ref: https://www.w3schools.com/python/gloss_python_date_format_codes.asp 

# DEBUG < INFO < WARNING < ERROR / EXCEPTION < CRITICAL
log_colors = {
    "DEBUG":"white",
    "INFO":"cyan",
    "WARNING":"yellow",
    "ERROR":"red",
    "CRITICAL":"purple",
}

colorama.init()
add_logging_level("OK", logging.INFO+1, "green")

logger_file_handler = None
logger_console_handler = None

if __name__ == "__main__":
    logger = create_logger(save_log=False)
    logger.debug("A quirky message only developers care about")
    logger.info("Curious users might want to know this")
    logger.warning("Something is wrong and any user should be informed")
    logger.error("Serious stuff, this is red for a reason")
    logger.critical("OH NO everything is on fire")
else:
    logger = create_logger(save_log=False)