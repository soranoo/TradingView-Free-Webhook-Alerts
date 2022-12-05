import re
import json
import requests
from requests.adapters import HTTPAdapter, Retry
from datetime import datetime

# =====================================
# SETTING
# =====================================

webhook_urls = [
  r"https://yourwebhook.com",
  #r"https://yourwebhook2.com",
  #r"https://yourwebhook3.com",
]

# vv for logging (fill in the webhook URL if you need)
discord_webhook_url = r""

# 4 = info, ok, warning, error
# 3 = ok, warning, error
# 2 = warning, error
# 1 = error only
# 0 = OFF
log_level = 4



# =====================================
# CODE
# =====================================

show_welcome_msg = False

url_regex = "https?://([A-Za-z_0-9.-]+).*"

dc_embeds_sample = [{
    "type":"rich",
    "title": "",
    "description": "",
    "color": 5533306,
    "footer": {
        "text": "Developed by Freeman(soranoo)",
        "icon_url": "https://avatars.githubusercontent.com/u/46896789?v=4"
      },
    }]

class log:
    def info(payload):
        if (log_level < 4 or log_level < 0):
            return
        embeds = dc_embeds_sample.copy()
        embeds[0]["title"] = "INFO"
        embeds[0]["description"] = payload
        embeds[0]["color"] = 5533306
        send_msg_to_dc("", embeds)

    def ok(payload:str):
        if (log_level < 3 or log_level < 0):
            return
        embeds = dc_embeds_sample.copy()
        embeds[0]["title"] = "OK"
        embeds[0]["description"] = payload
        embeds[0]["color"] = 5763719
        send_msg_to_dc("", embeds)

    def warning(payload:str):
        if (log_level < 2 or log_level < 0):
            return
        embeds = dc_embeds_sample.copy()
        embeds[0]["title"] = "WARNING"
        embeds[0]["description"] = payload
        embeds[0]["color"] = 16776960
        send_msg_to_dc("", embeds)

    def error(payload:str):
        if (log_level < 1 or log_level < 0):
            return
        embeds = dc_embeds_sample.copy()
        embeds[0]["title"] = "ERROR"
        embeds[0]["description"] = payload
        embeds[0]["color"] = 15548997
        send_msg_to_dc("", embeds)

def extract_domain_name(url:str):
    m = re.search(url_regex, url)
    if m:
        return m.group(1)
    return None

def post_request(webhook_url:str, payload:str or json, auto_json_dumps:bool = True):
    headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
    data = json.dumps(payload) if auto_json_dumps else payload
    # start a session
    session = requests.Session()
    # set retry policy
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    # add adapter to session
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    # send request
    response = session.post(webhook_url, data=data, headers=headers)
    return response

def send_msg_to_dc(message, embeds=None):
    if (len(discord_webhook_url.strip()) == 0):
        return # empty URL
    if extract_domain_name(discord_webhook_url) is None:
        print("Invalid Discord Webhook URL")
        return
    payload = json.dumps({'content': f"{message}", "embeds":embeds} )
    post_request(discord_webhook_url, payload, False)

def send_webhook(payload:str):
    # load json
    try:
        payload = json.loads(payload)
    except ValueError as err:
        pass
    # loop
    for webhook_url in webhook_urls:
        domain = extract_domain_name(webhook_url)
        if domain is None:
            log.warning(f"Send webhook failed.\nReason: invalid URL <{webhook_url}>\nContent: {payload}")
            continue
        currentTime = datetime.now()
        response = post_request(webhook_url, payload)
        time_used = (datetime.now()-currentTime).total_seconds() * 1000
        if (response.status_code == 200):
            log.ok(f"Webhook Sent!\n\nProcess Time: {time_used}ms\nDomain: {domain}\nFull URL: {webhook_url}\nContent: {payload}")
        else:
            log.error(f"Send webhook failed.\nReason: {response.text}\nStatus: {response.status_code}\n\nDomain: {domain}\nFull URL: {webhook_url}\nContent: {payload}")


def handler(pd: "pipedream"):
    global show_welcome_msg
    if not show_welcome_msg:
        log.info("You are GOOD to go!\n\n")
        show_welcome_msg = True
    # extract signal from previous steps
    content = pd.steps["trigger"]["event"]["body"]["text"]
    send_webhook(content)