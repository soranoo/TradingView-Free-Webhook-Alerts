import pyfiglet
import logging
from rich import print as cprint
from rich import traceback

from src import config, log , create_logger, shutdown
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

ngrok_auth_token:str | None = config.get("ngrok_auth_token")
ngrok_api_server_auth_key:str | None = config.get("ngrok_api_server_auth_key")

discord_log:bool = config.get("discord_log", False)
discord_webhook_url:str | None = config.get("discord_webhook_url")

log_with_colors:bool = config.get("log_color", True)
log_with_time_zone:bool = config.get("log_time_zone", False)
save_log:bool = config.get("log_save", True)
log_with_full_colors:bool = config.get("log_full_color", True)

config_version:str | None = config.get("config_version")

# ---------------* Main *---------------
__version__ = "2.6.4"
expect_config_version = "1.0.2"
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
        if not discord_webhook_url:
            log.error("Discord webhook URL is not set, please set it in the config file.")
            shutdown()
        log.addHandler(DiscordLogHandler(discord_webhook_url))
    if mode_traditional:
        # Config check before EmailSignalExtraction
        missing = []
        if not email_address:
            missing.append("email_address")
        if not login_password:
            missing.append("login_password")
        if not imap_server_address:
            missing.append("imap_server_address")
        if not imap_server_port:
            missing.append("imap_server_port")
        if missing:
            log.error(f"Missing required email config: {', '.join(missing)}. Please set these in the config file.")
            shutdown()
        EmailSignalExtraction(
            email_address, login_password,
            imap_server_address, imap_server_port,
            imap_auto_reconnect, imap_auto_reconnect_wait
        ).main()
    else:
        if not ngrok_auth_token:
            log.error("Missing ngrok auth token, please set it in the config file.")
            shutdown()
        else:
            NgrokSignalRedirect(ngrok_auth_token, ngrok_api_server_auth_key).main()

if __name__ == "__main__":
    # welcome message
    cprint(pyfiglet.figlet_format("TradingView\nFree Webhook"))
    # startup check
    print(f"Version: {__version__}  |  Config Version: {config_version}")
    if(config_version != expect_config_version):
        log.error(f"The config file is outdated. Looking version {expect_config_version} but found {config_version}. Please update it to the latest version. (visit {github_config_toml_url})")
        shutdown()
    main()
