from .smart_import import try_import

try_import("flask")

from waitress import serve
from flask import Flask, request
from . import log, event_post, StoppableThread
import time
import requests
import secrets
import logging

#! Store API key in header is more secure than in URL

api_key = None
event_id_receive = None
START_PORT = 5000

app = Flask("API Server")
# app.config["DEBUG"] = True

# Route to receive JSON data
@app.route("/api", methods=["POST"])
def api():
    # verify API key
    if request.headers.get("X-API-KEY") != api_key:
        return "", 403
    data = request.json
    event_post(event_id_receive, data)
    return "", 204

@app.route("/ping", methods=["GET"])
def auth():
    auth = request.args.get("auth")
    return ("", 204) if auth == api_key else ("", 403)

def generate_api_key(num:int = 16) -> str:
    return secrets.token_urlsafe(num)

def start(event_id_port:str = None, event_id_rev:str = None):
    """
    ### Description ###
    Start the API server
    
    ### Parameters ###
        - `event_id_port`: Event ID to post the port number
        - `event_id_rev`: Event ID to post the received data
    """
    def _try_start_with(p:int):
        # start server
        serve(app, port=p, ident="API Server") # production server
        # app.run(port=p) # development server
        
    global api_key
    global event_id_receive
    log.info("Start port test...")
    port = START_PORT
    while True:
        log.info(f"Testing port {port}")
        
        # disable waitress logging to avoid double logging
        # ref: https://stackoverflow.com/a/73718530
        noop = logging.NullHandler()
        logging.getLogger().addHandler(noop)
        
        thread = StoppableThread(target=_try_start_with, args=(port,))
        thread.start()
        api_key = generate_api_key(32)
        time.sleep(1)
        rep = requests.get(f"http://127.0.0.1:{port}/ping?auth={api_key}")
        if rep.status_code == 204:
            log.info(f"Port {port} is free~")
            log.ok(f"API server is ready to use, port: {port}")
            api_key = generate_api_key(16)
            log.info(f"Your API key: {api_key}")
            log.info("Please add 'X-API-KEY' and the API key to the header as the header name and header value of your request.")
            if event_id_port:
                event_post(event_id_port, port)
            if event_id_rev:
                event_id_receive = event_id_rev
            break
        thread.stop()
        port += 1
    
if __name__ == "__main__":
    start()
