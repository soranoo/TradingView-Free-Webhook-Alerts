from src import try_import

try_import("pyfiglet")
try_import("rich")

import pyfiglet
import json
import time
import os

from rich import print as cprint
from rich import traceback
from datetime import date, datetime, timezone
# from bs4 import BeautifulSoup

from src import EmailListener
from src import config, send_post_request, StoppableThread
from src import log as tlog, DiscordEmbed
from src import project_main_directory
from src import event_subscribe, event_unsubscribe, event_post

traceback.install()

# ---------------* Config *---------------
mode_traditional = config.get("mode_traditional", True)

email_address = config.get("email_address")
login_password = config.get("login_password")
imap_server_address = config.get("imap_server_address")
imap_server_port = config.get("imap_server_port")
imap_auto_reconnect = config.get("imap_auto_reconnect")
imap_auto_reconnect_wait = config.get("imap_auto_reconnect_wait")

ngrok_auth_token = config.get("ngrok_auth_token")

webhook_urls = config.get("webhook_urls")

discord_log = config.get("discord_log")
discord_webhook_url = config.get("discord_webhook_url")

config_version = config.get("config_version")

tradingview_alert_email_address = ["noreply@tradingview.com"]

# ---------------* Main *---------------
program_version = "2.6.0"
expect_config_version = "1.0.0"
github_config_toml_url = "https://github.com/soranoo/TradingView-Free-Webhook-Alerts/blob/main/config.example.toml"

if not mode_traditional:
    try_import("pyngrok")
    from pyngrok import ngrok, conf as ngrok_conf
    from src import api_server_start

# 5 = debug, info, ok, warning, error
# 4 = info, ok, warning, error
# 3 = ok, warning, error
# 2 = warning, error
# 1 = error only
# 0 = OFF
log_level = 5

class Log:
    EVENT_ID_DC_LOG = "dc-log"
    
    def __init__(self) -> None:
        self.thread = StoppableThread(target=self._run_thread, args=())
        self.thread.start()
    
    def _run_thread(self):
        event_subscribe(self.EVENT_ID_DC_LOG, self._send_to_webhook)
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
    
    def _send_to_webhook(self, embed:DiscordEmbed):
        if not discord_log:
            return
        if not discord_webhook_url:
            log.warning("Discord webhook URL is not set.")
        embed.webhook_url = discord_webhook_url
        embed.send_to_webhook()
    
    def debug(self, payload:str):
        if (log_level < 5 or log_level < 0):
            tlog.debug(payload)
    
    def info(self, payload):
        if (log_level < 4 or log_level < 0):
            return
        embed = DiscordEmbed(title = "INFO", description = payload,
                            color = DiscordEmbed.Color.BLUE)
        event_post(self.EVENT_ID_DC_LOG, embed)
        tlog.info(payload)

    def ok(self, payload:str):
        if (log_level < 3 or log_level < 0):
            return
        embed = DiscordEmbed(title = "OK", description = payload,
                            color = DiscordEmbed.Color.GREEN)
        event_post(self.EVENT_ID_DC_LOG, embed)
        tlog.ok(payload)

    def warning(self, payload:str):
        if (log_level < 2 or log_level < 0):
            return
        embed = DiscordEmbed(title = "WARNING", description = payload,
                            color = DiscordEmbed.Color.YELLOW)
        event_post(self.EVENT_ID_DC_LOG, embed)
        tlog.warning(payload)

    def error(self, payload:str):
        if (log_level < 1 or log_level < 0):
            return
        embed = DiscordEmbed(title = "ERROR", description = payload,
                            color = DiscordEmbed.Color.RED)
        event_post(self.EVENT_ID_DC_LOG, embed)
        tlog.error(payload)
log = Log()
        
def shutdown(seconds:float = 10):
    log.warning(f"The program will shut down after {seconds}s...")
    time.sleep(seconds)
    log.thread.stop()
    exit()

def send_webhook(payload:str or dict):
    headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
    for webhook_url in webhook_urls:
        send_post_request(webhook_url, payload, headers)

class EmailSignalExtraction:
    last_email_uid = -1
    email_history = []
    loop_duration_sample = []
    displaying_loop_duration = False
            
    def add_email_to_history(self, email_uid:int) -> bool:
        if email_uid in self.email_history:
            return False
        self.email_history.append(email_uid)
        # if the length of email_history is greater than 20, delete the oldest one
        if len(self.email_history) > 20:
            del self.email_history[0]
        return True

    # <not in use>
    #// def extract_content_from_html(self, html:str) -> str:
    #//     try:
    #//         ctx = BeautifulSoup(html, "html.parser")
    #//         ctx = list(ctx.find_all("p"))[1].text
    #//     except Exception:
    #//         log.warning("No content found in email.")
    #//         ctx = ""
    #//     return ctx()

    def get_latest_email(self, el:EmailListener):
        try:
            for _, data in el.scrape(search_filter="ALL", latest_only=True, no_log=True).items():
                return data
        except Exception:
            return False

    def connect_imap_server(self) -> EmailListener:
        try:
            el = EmailListener(email=email_address, app_password=login_password, folder="INBOX", attachment_dir=os.path.join(project_main_directory, "temp", "emails"), logger=log.debug, imap_address=imap_server_address, imap_port=imap_server_port)
            # Log into the IMAP server
            el.login()
            return el
        except Exception as err:
            log.error(f"Here an error has occurred, reason: {err}")
            if (not imap_auto_reconnect):
                shutdown()
            log.warning(f"The program will try to reconnect after {imap_auto_reconnect_wait}s...")
            time.sleep(imap_auto_reconnect_wait)
            main()

    def on_email_received(self, el, msgs):
        for data in msgs.values():
            email_uid = int(data["Email_UID"])
            email_content = data["Plain_Text"]
            email_subject = data["Subject"]
            email_date = data["Date"]
            from_address = data["From_Address"]
            last_email_uid = self.email_history[-1]

            if (last_email_uid < 0):
                last_email_uid = email_uid-1

            if email_uid in self.email_history or email_uid <= last_email_uid:
                continue

            if from_address not in tradingview_alert_email_address:
                # if not target email... mark unseen?
                log.info(f"Email from {from_address} is not from TradingView, SKIP.")
                continue

            # check if JSON
            try:
                email_content = json.loads(email_content)
            except ValueError as err:
                pass
            # convert to JSON
            email_content = json.dumps(email_content)
            # send webhook
            log.info(f"Sending webhook alert<{email_subject}>, content: {email_content}")
            try:
                send_webhook(email_content)
                log.ok("Sent webhook alert successfully!")
                log.info(f"The whole process taken {round((datetime.now(timezone.utc) - email_date).total_seconds(), 3)}s.")
                self.add_email_to_history(email_uid)
            except Exception as err:
                log.error(f"Sent webhook failed, reason: {err}")
    
    def start(self):
        if (imap_auto_reconnect_wait <= 0):
            log.error("\"imap_auto_reconnect_wait\"(config.toml) must be greater than 0")
            shutdown()
            
        global last_email_uid
        log.info("Initializing...")
        el = self.connect_imap_server()
        latest_email = self.get_latest_email(el)
        last_email_uid = int(latest_email["Email_UID"]) if latest_email else False
        if (last_email_uid is not False):
            self.add_email_to_history(last_email_uid)
        else:
            self.add_email_to_history(-1)

        # Start listening to the inbox
        log.info(f"Listening to IMAP server({imap_server_address})...")
        el.listen(-1, process_func=self.on_email_received)
        
    def main(self):
        try:
            self.start()
        except KeyboardInterrupt:
            log.warning("The program has been stopped by user.")
            shutdown()
        except Exception as err:
            log.error(f"Here an error has occurred, reason: {err}")
            if (not imap_auto_reconnect):
                shutdown()
            log.warning(f"The program will try to reconnect after {imap_auto_reconnect_wait}s...")
            time.sleep(imap_auto_reconnect_wait)
            self.start()

class NgrokSignalRedirect:
    class _EventID:
        API_PORT = "api-port"
        API_REV = "api-rev"
    
    def calculate_seconds_to_now(self, date_str:str) -> float:
        """
        ### Description ###
        Calculate the number of seconds from the given date to now
        
        ### Parameters ###
            - `date` (str): The date string in the format of "%Y-%m-%dT%H:%M:%S.%fZ", eg. "2022-12-21T17:51:24.288Z"
        
        ### Returns ###
            - (float) The number of seconds from the given date to now.
        """
        # parse the timestamp string into a datetime object
        timestamp = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        # get the current time
        now = datetime.utcnow()
        # calculate the difference between the two times
        diff = now - timestamp
        # get and return the number of seconds from the difference
        return diff.total_seconds()
    
    def on_data_received(self, data:dict):
        if not isinstance(data, dict):
            log.info(f"Incorrect data({data}) format received, SKIP.")
            return
        from_address = data.get("from")
        email_subject = data.get("subject")
        email_content = data.get("content")
        receive_datetime = data.get("receive_datetime")
        print(receive_datetime)

        # validate the data
        if not from_address or not email_subject or not email_content or not receive_datetime:
            log.error(f"Received data is not valid, data: {data}")
            return
        elif from_address not in tradingview_alert_email_address:
            log.info(f"Email from {from_address} is not from TradingView, SKIP.")
            return         

        log.info(f"Sending webhook alert<{email_subject}>, content: {email_content}")
        try:
            send_webhook(email_content)
            log.ok("Sent webhook alert successfully!")
            log.info(f"The whole process taken {self.calculate_seconds_to_now(receive_datetime)}s.")
        except Exception as err:
            log.error(f"Sent webhook failed, reason: {err}")
        
    def setup_ngrok(self, port=int):
        log.info("Setting up ngrok...")
        ngrok.set_auth_token(ngrok_auth_token)
        ngrok_conf.get_default().log_event_callback = None # mute ngrok log
        http_tunnel = ngrok.connect(port, "http")
        log.info(f"Your ngrok URL: {http_tunnel.public_url}")
        event_unsubscribe(self._EventID.API_PORT, self.setup_ngrok)
        
    def setup_api_server(self):
        thread = StoppableThread(target=api_server_start, args=(self._EventID.API_PORT,))
        thread.start()
        
    def main(self):
        if not ngrok_auth_token:
            log.error("Missing ngrok auth token, please set it in the config file.")
            shutdown()
        event_subscribe(self._EventID.API_PORT, self.setup_ngrok)
        event_subscribe(self._EventID.API_REV, self.on_data_received)
        thread = StoppableThread(target=api_server_start, args=(self._EventID.API_PORT, self._EventID.API_REV))
        thread.start()
        thread.join()

def main():
    log.debug(f"Traditional mode: {mode_traditional}")
    if mode_traditional:
        EmailSignalExtraction().main()
    else:
        NgrokSignalRedirect().main()

if __name__ == "__main__":
    # welcome message
    cprint(pyfiglet.figlet_format("TradingView\nFree Webhook"))
    # startup check
    print(f"Version: {program_version}  |  Config Version: {config_version}")
    if(config_version != expect_config_version):
        log.error(f"The config file is outdated. Please update it to the latest version. (visit {github_config_toml_url})")
        shutdown()
    main()