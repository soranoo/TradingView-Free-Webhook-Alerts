import contextlib
import json
import os
import time
from datetime import datetime, timezone
from src import EmailListener, log, shutdown, project_main_directory, TRADINGVIEW_ALERT_EMAIL_ADDRESS
from src.broadcast import broadcast

class EmailSignalExtraction:
    # env
    imap_auto_reconnect: bool
    imap_auto_reconnect_wait: int
    email_address: str
    login_password: str
    imap_server_address: str
    imap_server_port: int
    
    last_email_uid = -1
    email_history = []
    loop_duration_sample = []
    displaying_loop_duration = False
    
    def __init__(self, 
                 email_address:str, 
                 login_password:str, 
                 imap_server_address:str, 
                 imap_server_port:int, 
                 imap_auto_reconnect:bool, 
                 imap_auto_reconnect_wait:int
                ):
        self.email_address = email_address
        self.login_password = login_password
        self.imap_server_address = imap_server_address
        self.imap_server_port = imap_server_port
        self.imap_auto_reconnect = imap_auto_reconnect
        self.imap_auto_reconnect_wait = imap_auto_reconnect_wait
    
            
    def add_email_to_history(self, email_uid: int) -> bool:
        if email_uid in self.email_history:
            return False
        self.email_history.append(email_uid)
        # if the length of email_history is greater than 20, delete the oldest one
        if len(self.email_history) > 20:
            del self.email_history[0]
        return True

    def get_latest_email(self, el: EmailListener):
        try:
            for _, data in el.scrape(search_filter="ALL", latest_only=True, no_log=True).items():
                return data
        except Exception:
            return False

    def connect_imap_server(self) -> EmailListener:
        try:
            el = EmailListener(email=self.email_address, app_password=self.login_password, folder="INBOX", attachment_dir=os.path.join(project_main_directory, ".temp", "emails"), logger=log.debug, imap_address=self.imap_server_address, imap_port=self.imap_server_port)
            # Log into the IMAP server
            el.login()
            return el
        except Exception as err:
            log.error(f"Here an error has occurred, reason: {err}")
            if not self.imap_auto_reconnect:
                shutdown()
            log.warning(f"The program will try to reconnect after {self.imap_auto_reconnect_wait}s...")
            time.sleep(self.imap_auto_reconnect_wait)
            self.main()

    def on_email_received(self, el, msgs):
        for data in msgs.values():
            email_uid = int(data["Email_UID"])
            email_content = data["Plain_Text"]
            email_subject = data["Subject"]
            email_date = data["Date"]
            from_address = data["From_Address"]
            last_email_uid = self.email_history[-1]

            if last_email_uid < 0:
                last_email_uid = email_uid - 1

            if email_uid in self.email_history or email_uid <= last_email_uid:
                continue

            if from_address not in TRADINGVIEW_ALERT_EMAIL_ADDRESS:
                log.info(f"Email from {from_address} is not from TradingView, SKIP.")
                continue

            with contextlib.suppress(ValueError):
                email_content = json.loads(email_content)
            email_content = json.dumps(email_content)
            log.info(f"Sending webhook alert<{email_subject}>, content: {email_content}")
            try:
                broadcast(email_content)
                log.info(f"The whole process taken {round((datetime.now(timezone.utc) - email_date).total_seconds(), 3)}s.")
                self.add_email_to_history(email_uid)
            except Exception as err:
                log.error(f"Sent webhook failed, reason: {err}")
    
    def start(self):
        if self.imap_auto_reconnect_wait <= 0:
            log.error("\"imap_auto_reconnect_wait\"(config.toml) must be greater than 0")
            shutdown()
            
        global last_email_uid
        log.info("Initializing...")
        el = self.connect_imap_server()
        latest_email = self.get_latest_email(el)
        last_email_uid = int(latest_email["Email_UID"]) if latest_email else False
        if last_email_uid is not False:
            self.add_email_to_history(last_email_uid)
        else:
            self.add_email_to_history(-1)

        log.info(f"Listening to IMAP server({self.imap_server_address})...")
        el.listen(-1, process_func=self.on_email_received)
        
    def main(self):
        try:
            self.start()
        except KeyboardInterrupt:
            log.warning("The program has been stopped by user.")
            shutdown()
        except Exception as err:
            log.error(f"Here an error has occurred, reason: {err}")
            if not self.imap_auto_reconnect:
                shutdown()
            log.warning(f"The program will try to reconnect after {self.imap_auto_reconnect_wait}s...")
            time.sleep(self.imap_auto_reconnect_wait)
            self.start()
