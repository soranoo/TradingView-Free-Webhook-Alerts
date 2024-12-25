import json
import time

from . import config, log, is_url_valid, send_post_request, plan_to_run_run_at
from . import POST_REQUEST_HEADERS, RETRY_AFTER_HEADER

webhook_urls:list[str] | None = config.get("webhook_urls")
tg_bot_token:str | None = config.get("tg_bot_token")
tg_chat_id:str | None = config.get("tg_chat_id")

if (tg_bot_token and not tg_chat_id) or (not tg_bot_token and tg_chat_id):
    log.error("Telegram bot token and chat ID must be both set or both empty.")
    exit()

# List broadcast methods
log.info("Broadcast methods:")
if webhook_urls:
    log.info(f"[+] Webhook: {len(webhook_urls)} URL(s) found.")
else :
    log.info("[-] Webhook: Disabled")
if tg_bot_token and tg_chat_id:
    log.info("[+] Telegram: ✅")
else:
    log.info("[-] Telegram: Disabled")

proxy_url = config.get("proxy_url")
proxies = {
    "http": proxy_url,
    "https": proxy_url
} if proxy_url else None

# Validate proxy URL
if proxies != None:
    if is_valid_url := is_url_valid(proxy_url):
        log.info(f"Using proxy: {proxy_url}")
    else:
        log.error(f"Invalid proxy URL: {proxy_url}")
        exit()

def send_webhook(payload:str | dict):
    """
    ### Description ###
    Send a webhook to the specified URL(s).
    
    ### Parameters ###
        - `payload` (str | dict): The content of the webhook to send
    """
    for webhook_url in webhook_urls:
        res = send_post_request(webhook_url, payload, POST_REQUEST_HEADERS, proxies=proxies)
        if res.status_code >= 200 and res.status_code < 300:
            log.ok(f"Sent webhook to {webhook_url} successfully, response code: {res.status_code}")
        elif retry_after := res.headers.get("Retry-After"):
            if res.status_code == 429:
                log.warning(f"Sent webhook to {webhook_url} failed, response code: {res.status_code}, Content: {payload}, Retry-After header({RETRY_AFTER_HEADER}) found, auto retry after {retry_after}s...")
                plan_to_run_run_at(time.time() + float(retry_after), send_webhook, payload)
                continue
            log.error(f"Sent webhook to {webhook_url} failed, response code: {res.status_code}, Content: {payload}.")

def send_msg_to_tg(payload:str | dict) -> None:
    """
    ### Description ###
    Send a message to the specified Telegram chat.
    
    ### Parameters ###
        - `payload` (str | dict): The content of the message to send

    ### Raises ###
        - ValueError: If message exceeds Telegram's length limit
    """
    if isinstance(payload, dict):
        payload = json.dumps(payload)
        
    if len(payload) > 4096:
        raise ValueError("Message exceeds Telegram's 4096 character limit")

    payload = json.dumps({"chat_id": f"{tg_chat_id}", "text": f"{payload}"})
    try:
        response = send_post_request(
            f"https://api.telegram.org/bot{tg_bot_token}/sendMessage",
            payload,
            POST_REQUEST_HEADERS,
            proxies=proxies
        )
        if response.status_code >= 400:
            log.error(f"Telegram API error: {response.text}")
    except Exception as e:
        log.error(f"Failed to send Telegram message: {str(e)}")

def broadcast(payload:str | dict):
    """
    ### Description ###
    Broadcast the payload to all available methods.
    
    ### Parameters ###
        - `payload` (str | dict): The content to broadcast
    """
    if webhook_urls:
        send_webhook(payload)
    if len(tg_bot_token.strip()) and len(tg_chat_id.strip()):
        send_msg_to_tg(payload)
    log.info("Broadcasted successfully.")
