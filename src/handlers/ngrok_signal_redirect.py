from datetime import datetime, timezone
from src import log, shutdown, event_subscribe, event_unsubscribe, api_server_start, StoppableThread, TRADINGVIEW_ALERT_EMAIL_ADDRESS
from src.smart_import import try_import
from src.broadcast import broadcast

class NgrokSignalRedirect:
    class _EventID:
        API_PORT = "api-port"
        API_REV = "api-rev"
        
    # env
    ngrok_auth_token: str
        
    def __init__(self, ngrok_auth_token: str):
        self.ngrok_auth_token = ngrok_auth_token
    
    def calculate_seconds_to_now(self, date_str: str) -> float:
        timestamp = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        now = datetime.now(timezone.utc)
        diff = now - timestamp
        return diff.total_seconds()
    
    def on_data_received(self, data: dict):
        if not isinstance(data, dict):
            log.info(f"Incorrect data({data}) format received, SKIP.")
            return
        from_address = data.get("from")
        email_subject = data.get("subject")
        email_content = data.get("content")
        receive_datetime = data.get("receive_datetime")
        print(receive_datetime)

        if not from_address or not email_subject or not email_content or not receive_datetime:
            log.error(f"Received data is not valid, data: {data}")
            return
        elif from_address not in TRADINGVIEW_ALERT_EMAIL_ADDRESS:
            log.info(f"Email from {from_address} is not from TradingView, SKIP.")
            return         

        log.info(f"Sending webhook alert<{email_subject}>, content: {email_content}")
        broadcast(email_content)
        log.info(f"The whole process taken {self.calculate_seconds_to_now(receive_datetime)}s.")
        
    def setup_ngrok(self, port: int):
        try_import("pyngrok")
        from pyngrok import ngrok, conf as ngrok_conf
    
        log.info("Setting up ngrok...")
        ngrok.set_auth_token(self.ngrok_auth_token)
        ngrok_conf.get_default().log_event_callback = None
        http_tunnel = ngrok.connect(port, "http")
        log.info(f"Your ngrok URL: {http_tunnel.public_url}")
        event_unsubscribe(self._EventID.API_PORT, self.setup_ngrok)
        
    def setup_api_server(self):
        thread = StoppableThread(target=api_server_start, args=(self._EventID.API_PORT,))
        thread.start()
        
    def main(self):
        if not self.ngrok_auth_token:
            log.error("Missing ngrok auth token, please set it in the config file.")
            shutdown()
        event_subscribe(self._EventID.API_PORT, self.setup_ngrok)
        event_subscribe(self._EventID.API_REV, self.on_data_received)
        thread = StoppableThread(target=api_server_start, args=(self._EventID.API_PORT, self._EventID.API_REV))
        thread.start()
        thread.join()