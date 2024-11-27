from src import shutdown

import pyfiglet
import logging

from rich import print as cprint
from rich import traceback

from src import config
from src import log , create_logger
from src.handlers.discord_log_handler import DiscordLogHandler
from src.handlers.email_signal_extraction import EmailSignalExtraction
from src.handlers.ngrok_signal_redirect import NgrokSignalRedirect

traceback.install()

# ---------------* Config *---------------
mode_traditional = config.get("mode_traditional", True)

email_address:str | None = config.get("email_address")
login_password:str | None = config.get("login_password")
imap_server_address:str | None = config.get("imap_server_address")
imap_server_port:int | None = config.get("imap_server_port")
imap_auto_reconnect:bool | None = config.get("imap_auto_reconnect")
imap_auto_reconnect_wait:int | None = config.get("imap_auto_reconnect_wait")

ngrok_auth_token = config.get("ngrok_auth_token")

discord_log = config.get("discord_log")
discord_webhook_url = config.get("discord_webhook_url")

log_with_colors = config.get("log_color")
log_with_time_zone = config.get("log_time_zone")
save_log = config.get("log_save")
log_with_full_colors = config.get("log_full_color")

config_version = config.get("config_version")

# ---------------* Main *---------------
__version__ = "2.6.3"
expect_config_version = "1.0.1"
github_config_toml_url = "https://github.com/soranoo/TradingView-Free-Webhook-Alerts/blob/main/config.example.toml"

def main():
    log.debug(f"Traditional mode: {mode_traditional}")
    create_logger(
        save_log=save_log, color_print=log_with_colors,
        print_log_msg_color=log_with_full_colors,
        included_timezone=log_with_time_zone,
        log_level=logging.DEBUG, rebuild_mode=True,
        rebuild_logger=log
    )
    if discord_log:
        log.addHandler(DiscordLogHandler())
    if mode_traditional:
        EmailSignalExtraction(
            email_address, login_password,
            imap_server_address, imap_server_port,
            imap_auto_reconnect, imap_auto_reconnect_wait
                              ).main()
    else:
        NgrokSignalRedirect(ngrok_auth_token).main()

if __name__ == "__main__":
    # welcome message
    cprint(pyfiglet.figlet_format("TradingView\nFree Webhook"))
    # startup check
    print(f"Version: {__version__}  |  Config Version: {config_version}")
    if(config_version != expect_config_version):
        log.error(f"The config file is outdated. Looking version {expect_config_version} but found {config_version}. Please update it to the latest version. (visit {github_config_toml_url})")
        shutdown()
    main()
