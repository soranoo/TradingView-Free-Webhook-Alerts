import toml
import pyfiglet
import json
import requests
import time
import os

from rich import print as cprint
from rich import traceback
from imap_tools import MailBox
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

from src.logger import log, Colorcode

traceback.install()
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) # get current directory

# ---------------* Common *---------------
config = toml.load(os.path.join(__location__, "config.toml"))
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
    return response

def send_webhook(payload:str):
    headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }
    for webhook_url in webhook_urls:
        post_request(webhook_url, payload, headers)

def display_loop_duration(duration:float):
    global loop_duration_sample
    global displaying_loop_duration

    prefix = "Average loop duration(smaller is better): "
    round_num = 5
    max_sample_num = 20
    if duration != -1:
        displaying_loop_duration = True
        def average(array):
            return round(sum(array)/len(array), round_num)
        def fillZero(num):
            if "." not in str(num):
                return str(num)+"."+"0"*round_num
            str_diff = round_num - len(str(num).split(".")[1])
            if str_diff > 0:
                num = str(num)+"0"*str_diff
            return num
        duration = duration.total_seconds()
        loop_duration_sample.append(duration)
        # control number of sample
        if len(loop_duration_sample) > max_sample_num:
            del loop_duration_sample[0]
        # get average duration
        avg = str(fillZero(average(loop_duration_sample)))
        output = prefix+avg+"s"
    else:
        displaying_loop_duration = False
        avg = str("0."+"0"*(round_num+3))
        textCount = len(prefix+avg)
        output = " "*textCount
    print(f"{Colorcode.magenta}{output}{Colorcode.reset}", end="\r")
        
def add_email_to_history(email_uid:int):
    global email_history
    if email_uid in email_history:
        return False
    email_history.append(email_uid)
    # if the length of email_history is greater than 20, delete the oldest one
    if len(email_history) > 20:
        del email_history[0]
    return True

def get_latest_email(mailbox:MailBox):
    try:
        for email in mailbox.fetch(limit=1, reverse=True):
            return email
    except:
        return False

def connect_imap_server():
    try:
        mailbox = MailBox(host=imap_server_address, port=imap_server_port)
        mailbox.login(email_address, login_password, initial_folder="INBOX")
        return mailbox
    except Exception as err:
        log.error(f"Here an error has occurred, reason: {err}")
        if (not imap_auto_reconnect):
            shutdown()
        log.warning(f"The program will try to reconnect after {imap_auto_reconnect_wait}s...")
        time.sleep(imap_auto_reconnect_wait)
        main()

def close_imap_connection(mailbox):
    mailbox.logout()

def main():
    global last_email_uid
    log.info("Initializing...")
    mailbox = connect_imap_server()
    latest_email = get_latest_email(mailbox)
    last_email_uid = int(latest_email.uid) if latest_email else False
    close_imap_connection(mailbox)
    log.info(f"Listening to IMAP server({imap_server_address})...")
    while True:
        # ref: https://github.com/ikvk/imap_tools#actions-with-emails
        start_time = datetime.now()
        mailbox = connect_imap_server()
        latest_email = get_latest_email(mailbox)
        latest_emailUid = int(latest_email.uid) if latest_email else False
        add_email_to_history(latest_emailUid)
        # check if inbox turn from empty to not empty
        if not last_email_uid and latest_emailUid >= 0:
            # giving a previous email uid
            last_email_uid = latest_emailUid-1
        uidDifferent = (latest_emailUid-last_email_uid) if latest_emailUid else -1
        if uidDifferent > 0:
            latest_emails = mailbox.fetch(limit=uidDifferent, reverse=True)
            for email in latest_emails:
                if (email.uid in email_history) or int(email.uid) <= last_email_uid:
                    continue
                if email.from_ in tradingview_alert_email_address:
                    # get email content
                    if email.text == "":
                        try:
                            ctx = BeautifulSoup(email.html, "html.parser")
                            ctx = list(ctx.find_all("p"))[1].text
                        except:
                            log.warning("No content found in email.")
                            ctx = ""
                    else:
                        ctx = email.text
                    # check if json
                    try:
                        ctx = json.loads(ctx)
                    except:
                        ctx = email.text
                    # stop display loop duration
                    if displaying_loop_duration:
                            display_loop_duration(-1)
                    # send webhook
                    log.info(f"Sending webhook alert<{email.subject}>, content: {ctx}")
                    try:
                        send_webhook(ctx)
                        log.ok("Sent webhook alert successfully!")
                        log.info(f"The whole process taken {round(abs(datetime.now(timezone.utc)-email.date).total_seconds(),3)}s.")
                        add_email_to_history(email.uid)
                    except Exception as err:
                        log.error(f"Sent webhook failed, reason: {err}")
                else:
                    # if not target email... mark unseen?
                    # code
                    pass
        else:
            pass
        display_loop_duration(datetime.now()-start_time)
        last_email_uid = latest_emailUid
        close_imap_connection(mailbox)

if (imap_auto_reconnect_wait <= 0):
    log.error("\"imap_auto_reconnect_wait\"(config.toml) must be greater than 0")
    shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("The program has been stopped by user.")
        shutdown()
