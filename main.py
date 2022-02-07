import os
import toml
import pyfiglet
import json
import requests
import time

from rich import print as cprint
from rich import traceback

from src.logger import log, Colorcode

from imap_tools import MailBox
from datetime import datetime, timezone

traceback.install()

# ---------------* Common *---------------
cwd = os.getcwd()+"/"
config = toml.load("config.toml")
email_address = config.get("email_address")
login_password = config.get("login_password")
imap_server_address = config.get("imap_server_address")
imap_server_port = config.get("imap_server_port")
webhook_urls = config.get("webhook_urls")

tradingview_alert_email_address = ["noreply@tradingview.com"]

# ---------------* Main *---------------

last_email_uid = -1
loop_duration_sample = []
displaying_loop_duration = False

# welcome message
print(pyfiglet.figlet_format("TradingView\nFree Webhook"))


def send_webhook(payload):
    headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }
    for webhook_url in webhook_urls:
        requests.post(webhook_url, data=json.dumps(payload), headers=headers)

def display_loop_duration(duration):
    global loop_duration_sample
    global displaying_loop_duration

    prefix = "Average loop duration(smaller is better): "
    roundNum = 5
    maxSampleNum = 20
    if duration != -1:
        displaying_loop_duration = True
        def average(array):
            return round(sum(array)/len(array), roundNum)
        def fillZero(num):
            if "." not in str(num):
                return str(num)+"."+"0"*roundNum
            strDiff = roundNum - len(str(num).split(".")[1])
            if strDiff > 0:
                num = str(num)+"0"*strDiff
            return num
        duration = duration.total_seconds()
        loop_duration_sample.append(duration)
        # control number of sample
        if len(loop_duration_sample) > maxSampleNum:
            del loop_duration_sample[0]
        # get average duration
        avg = str(fillZero(average(loop_duration_sample)))
        output = prefix+avg+"s"
    else:
        displaying_loop_duration = False
        avg = str("0."+"0"*(roundNum+3))
        textCount = len(prefix+avg)
        output = " "*textCount
    print(f"{Colorcode.magenta}{output}{Colorcode.reset}", end="\r")
        

def get_latest_email(mailbox):
    for email in mailbox.fetch(limit=1, reverse=True):
        return email

def connect_imap_server():
    try:
        mailbox = MailBox(host=imap_server_address, port=imap_server_port)
        mailbox.login(email_address, login_password, initial_folder="INBOX")
        return mailbox
    except Exception as err:
        log.error(f"Here an error has occurred, reason: {err}")
        log.warning("The program will shut down after 10s...")
        time.sleep(10)
        exit()

def close_imap_connection(mailbox):
    mailbox.logout()

def main():
    global last_email_uid
    log.info("Initializing...")
    mailbox = connect_imap_server()
    last_email_uid = get_latest_email(mailbox).uid
    close_imap_connection(mailbox)
    log.info(f"Listening to IMP server({imap_server_address})...")
    while True:
        # ref: https://github.com/ikvk/imap_tools#actions-with-emails
        startTime = datetime.now()
        mailbox = connect_imap_server()
        latestEmailUid = get_latest_email(mailbox).uid
        uidDifferent = int(latestEmailUid)-int(last_email_uid)
        if uidDifferent > 0:
            latestEmails = mailbox.fetch(limit=uidDifferent, reverse=True)
            for email in latestEmails:
                if email.from_ in tradingview_alert_email_address:
                    if displaying_loop_duration:
                            display_loop_duration(-1)
                    log.info(f"Sending webhook alert<{email.subject}>..., content: {email.text}")
                    try:
                        send_webhook(email.text)
                        log.ok("Sent webhook alert successfully!")
                        log.info(f"The whole process taken {round(abs(datetime.now(timezone.utc)-email.date).total_seconds(),3)}s.")
                    except Exception as err:
                        log.error(f"Sent webhook failed, reason: {err}")
                else:
                    # if not target email... mark unseen?
                    # code
                    pass
        else:
            pass
        display_loop_duration(datetime.now()-startTime)
        last_email_uid = latestEmailUid
        close_imap_connection(mailbox)


if __name__ == "__main__":
    main()
