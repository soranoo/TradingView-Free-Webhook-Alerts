from .smart_import import try_import
try_import("requests")
try_import("discord", pip_package_name="discord.py")

import requests
import json
from discord.embeds import Embed as OrginalEmbed
from .network import send_post_request

class Embed(OrginalEmbed):
    class Color:
        # ref: https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812
        AQUA				= 1752220	#1ABC9C
        DARKAQUA			= 1146986	#11806A
        GREEN				= 5763719	#57F287
        DARKGREEN			= 2067276	#1F8B4C
        BLUE				= 3447003	#3498DB
        DARKBLUE			= 2123412	#206694
        PURPLE				= 10181046	#9B59B6
        DARKPURPLE			= 7419530	#71368A
        LUMINOUSVIVIDPINK	= 15277667	#E91E63 LuminousVividPink
        DARKVIVIDPINK		= 11342935	#AD1457 DarkVividPink
        GOLD				= 15844367	#F1C40F
        DARKGOLD			= 12745742	#C27C0E DarkGold
        ORANGE				= 15105570	#E67E22
        DARKORANGE			= 11027200	#A84300 DarkOrange
        RED					= 15548997	#ED4245
        DARKRED				= 10038562	#992D22 DarkRed
        GREY				= 9807270	#95A5A6
        DARKGREY			= 9936031	#979C9F DarkGrey
        DARKERGREY			= 8359053	#7F8C8D DarkerGrey
        LIGHTGREY			= 12370112	#BCC0C0 LightGrey
        NAVY				= 3426654	#34495E
        DARKNAVY			= 2899536	#2C3E50 DarkNavy
        YELLOW				= 16776960	#FFFF00
        
        WHITE				= 16777215	#FFFFFF
        GREYPLE				= 10070709	#99AAB5
        BLACK				= 2303786	#23272A
        DARKBUTNOTBLACK		= 2895667	#2C2F33 DarkButNotBlack
        NOTQUITEBLACK		= 2303786	#23272A NotQuiteBlack
        BLURPLE				= 5793266	#5865F2
        FUCHSIA				= 15418782	#EB459E
    
    def __init__(self, **kwargs):
        self.color = kwargs.get("color", Embed.Color.WHITE)
        self.webhook_url = kwargs.get("webhook_url", None)
        # remove webhook_url from kwargs because it is a new attribute
        if "webhook_url" in kwargs:
            del kwargs["webhook_url"]
        super().__init__(**kwargs)
        
    def add_webhook_url(self, url:str):
        self.webhook_url = url
        
    def send_to_webhook(self)->requests.models.Response:
        if self.webhook_url is None:
            raise ValueError("No webhook URL provided")
        return send_post_request(self.webhook_url, json.dumps({"embeds": [self.to_dict()]}))

def send_message_to_webhook(url:str, message:str, embeds:list[dict] = None):
    payload = json.dumps({"content": message, "embeds": embeds} )
    return send_post_request(url, payload)
