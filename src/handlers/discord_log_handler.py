import logging
from queue import Queue
from src import DiscordEmbed, StoppableThread, log

class DiscordLogHandler(logging.Handler):
    """
    A log handler that will send the log record to the Discord.
    """
    
    discord_webhook_url = None
    
    def __init__(self, discord_webhook_url: str):
        super().__init__(level=logging.INFO)
        self.queue = Queue()
        self.thread = StoppableThread(target=self._thread_main, args=(self.queue,))
        self.thread.start()
        self.discord_webhook_url = discord_webhook_url
    
    def _thread_main(self, queue):
        while True:
            # get the next log embed from the queue
            embed = queue.get()

            # send the log embed to Discord
            self._send_to_webhook(embed)

            # mark the log embed as processed
            queue.task_done()
    
    def _send_to_webhook(self, embed: DiscordEmbed):
        if not self.discord_webhook_url:
            log.warning("Discord webhook URL is not set.")
        embed.webhook_url = self.discord_webhook_url
        embed.send_to_webhook()
    
    def emit(self, record):
        embed = None
        
        if record.levelname == "INFO":
            embed = DiscordEmbed(title="INFO", description=record.msg, color=DiscordEmbed.Color.BLUE)
        elif record.levelname == "OK":
            embed = DiscordEmbed(title="OK", description=record.msg, color=DiscordEmbed.Color.GREEN)
        elif record.levelname == "WARNING":
            embed = DiscordEmbed(title="WARNING", description=record.msg, color=DiscordEmbed.Color.YELLOW)
        elif record.levelname == "ERROR":
            embed = DiscordEmbed(title="ERROR", description=record.msg, color=DiscordEmbed.Color.RED)
        elif record.levelname == "CRITICAL":
            embed = DiscordEmbed(title="CRITICAL", description=record.msg, color=DiscordEmbed.Color.PURPLE)
        
        if not embed:
            return
        self.queue.put(embed)
        