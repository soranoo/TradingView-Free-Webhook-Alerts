import os
import toml
import pyfiglet
import json
import requests
import time

from rich import print as cprint
from rich import traceback
from imap_tools import MailBox
from datetime import datetime, timezone
from bs4 import BeautifulSoup

from src.logger import log, Colorcode


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
last_emails = []
loop_duration_sample = []
displaying_loop_duration = False

# welcome message
cprint(pyfiglet.figlet_format("TradingView\nFree Webhook"))


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
        log.warning("The program will shut down after 10s...")
        time.sleep(10)
        exit()

def close_imap_connection(mailbox):
    mailbox.logout()

def main():
    global last_email_uid
    log.info("Initializing...")
    mailbox = connect_imap_server()
    latestEmail = get_latest_email(mailbox)
    last_email_uid = int(latestEmail.uid) if latestEmail else False
    close_imap_connection(mailbox)
    log.info(f"Listening to IMP server({imap_server_address})...")
    while True:
        # ref: https://github.com/ikvk/imap_tools#actions-with-emails
        startTime = datetime.now()
        mailbox = connect_imap_server()
        latestEmail = get_latest_email(mailbox)
        latestEmailUid = int(latestEmail.uid) if latestEmail else False
        # check if inbox turn from empty to not empty
        if not last_email_uid and latestEmailUid >= 0:
            # giving a previous email uid
            last_email_uid = latestEmailUid-1
        uidDifferent = (latestEmailUid-last_email_uid) if latestEmailUid else -1
        if uidDifferent > 0:
            latestEmails = mailbox.fetch(limit=uidDifferent, reverse=True)
            last_emails = []
            for email in latestEmails:
                if email in last_emails:
                    log.warning(f"Duplicate email found: {email.uid}")
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
                        last_emails.append(email)
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
    try:
        main()
    except KeyboardInterrupt:
        log.warning("The program has been stopped by user.")
        log.warning("The program will shut down after 10s...")
        time.sleep(10)
        exit()
