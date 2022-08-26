import pyfiglet
import json
import requests
import time
import os

from rich import print as cprint
from rich import traceback
from datetime import date, datetime, timezone
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

from src import config, http_status
from src import log, Colorcode, add_logging_level, log_levels
from src import EmailListener
from src import project_main_directory

traceback.install()

# ---------------* Config *---------------
email_address = config.get("email_address")
login_password = config.get("login_password")
imap_server_address = config.get("imap_server_address")
imap_server_port = config.get("imap_server_port")
imap_auto_reconnect = config.get("imap_auto_reconnect")
imap_auto_reconnect_wait = config.get("imap_auto_reconnect_wait")
webhook_urls = config.get("webhook_urls")

tradingview_alert_email_address = ["noreply@tradingview.com"]

# ---------------* Main *---------------
# increase retries number
requests.adapters.DEFAULT_RETRIES = 5
last_email_uid = -1
email_history = []
loop_duration_sample = []
displaying_loop_duration = False

# welcome message
cprint(pyfiglet.figlet_format("TradingView\nFree Webhook"))

def shutdown(seconds:float = 10):
    log.warning(f"The program will shut down after {seconds}s...")
    time.sleep(seconds)
    exit()

def post_request(webhook_url:str, payload:str, headers:str):
    # ref: https://bobbyhadz.com/blog/python-requets-max-retries-exceeded-with-url
    # start a session
    session = requests.Session()
    # set retry policy
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    # add adapter to session
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    # send request
    response = session.post(webhook_url, data=json.dumps(payload), headers=headers)
    if (response.status_code != None):
        log.debug(f"Webhook response: <{response.status_code}>: {http_status[str(response.status_code)]}")
    return response

def send_webhook(payload:str):
    headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }
    for webhook_url in webhook_urls:
        post_request(webhook_url, payload, headers)
        
def add_email_to_history(email_uid:int) -> bool:
    global email_history
    if email_uid in email_history:
        return False
    email_history.append(email_uid)
    # if the length of email_history is greater than 20, delete the oldest one
    if len(email_history) > 20:
        del email_history[0]
    return True

# not in use
def extract_content_from_html(html:str) -> str:
    try:
        ctx = BeautifulSoup(html, "html.parser")
        ctx = list(ctx.find_all("p"))[1].text
    except:
        log.warning("No content found in email.")
        ctx = ""
    return ctx()

def get_latest_email(el:EmailListener):
    try:
        for _, data in el.scrape(search_filter="ALL", latest_only=True, no_log=True).items():
            return data
    except:
        return False

def connect_imap_server() -> EmailListener:
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

def on_email_received(el, msgs):
    for data in msgs.values():
        email_uid = int(data["Email_UID"])
        email_content = data["Plain_Text"]
        email_subject = data["Subject"]
        email_date = data["Date"]
        from_address = data["From_Address"]
        last_email_uid = email_history[-1]

        if (last_email_uid < 0):
            last_email_uid = email_uid-1

        if (email_uid in email_history) or int(email_uid) <= last_email_uid:
            continue

        if from_address not in tradingview_alert_email_address:
            # if not target email... mark unseen?
            log.info(f"Email from {from_address} is not from TradingView, SKIP.")
            continue

        # check if json
        try:
            email_content = json.loads(email_content)
        except:
            pass
        # send webhook
        log.info(f"Sending webhook alert<{email_subject}>, content: {email_content}")
        try:
            send_webhook(email_content)
            log.ok("Sent webhook alert successfully!")
            log.info(f"The whole process taken {round((datetime.now(timezone.utc) - email_date).total_seconds(), 3)}s.")
            add_email_to_history(email_uid)
        except Exception as err:
            log.error(f"Sent webhook failed, reason: {err}")

def main():
    global last_email_uid
    log.info("Initializing...")
    el = connect_imap_server()
    latest_email = get_latest_email(el)
    last_email_uid = int(latest_email["Email_UID"]) if latest_email else False
    if (last_email_uid is not False):
        add_email_to_history(last_email_uid)
    else:
        add_email_to_history(-1)

    # Start listening to the inbox
    log.info(f"Listening to IMAP server({imap_server_address})...")
    el.listen(-1, process_func=on_email_received)

if (imap_auto_reconnect_wait <= 0):
    log.error("\"imap_auto_reconnect_wait\"(config.toml) must be greater than 0")
    shutdown()

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        log.error(f"Here an error has occurred, reason: {err}")
        if (not imap_auto_reconnect):
            shutdown()
        log.warning(f"The program will try to reconnect after {imap_auto_reconnect_wait}s...")
        time.sleep(imap_auto_reconnect_wait)
        main()
    except KeyboardInterrupt:
        log.warning("The program has been stopped by user.")
        shutdown()