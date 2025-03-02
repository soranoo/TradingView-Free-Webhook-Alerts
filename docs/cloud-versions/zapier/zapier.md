# Getting Started with [zapier]((https://zapier.com/))

[🔙 Back to cloud-versions.md](/docs/cloud-versions/cloud-versions.md)

## 🌻 Shortcuts
- [Requirements](#-requirements)
- [Setup](#-setup)
- [Configuration](#-configuration)

## ⚓ Requirements
* A [TradingView](https://www.tradingview.com/) account
* A [zapier](https://zapier.com/) account
* A [Discord](https://discord.com/) account (optional)

## 👣 Setup
1. Login to [zapier](https://zapier.com/) and create a new workflow (Zap).
![img](imgs/setup_step_img_01.png)
2. Press into the trigger node.
![img](imgs/setup_step_img_02.png)
3. Select `Emails` as the trigger.
![img](imgs/setup_step_img_03.png)
4. Press the `Choose an event` box then select `New inbound email`.
![img](imgs/setup_step_img_04.png)
5. Press the `Continue` button.
6. Enter your custom email address and press the `Continue` button.
![img](imgs/setup_step_img_05.png)
7. Copy the email address given by zapier.
![img](imgs/setup_step_img_06.png)
8. Open your TradingView account and chanage the `Alternate email for alerts` to the email address given by zapier.
![img](imgs/setup_step_img_07.png)
9. Paste the copied email address into the `Account verification` dialog email field and press `Get code` button.
![img](imgs/setup_step_img_08.png)
10. Back to zapier and press the `Test trigger` button.
![img](imgs/setup_step_img_09.png)
11. Press `Email A` and scroll down to find the verification code (from `Body Plain`).
![img](imgs/setup_step_img_10.png)
12. Paste the verification code into the TradingView `Account verification` dialog and press the `Submit` button.
![img](imgs/setup_step_img_11.png)
13. Back to zapier and close the side panel.
14. Select the action node.
![img](imgs/setup_step_img_12.png)
15. Search for `Code` and select it.
![img](imgs/setup_step_img_13.png)
16. Press the `Choose an event` box then select `Run Python`.
![img](imgs/setup_step_img_14.png)
17. Press the `Continue` button.
18. Add the following variables to the `Input Data` table.
    | Key | Value |
    | --- | --- |
    | signal | `{{Body Plain}}` |
    | from_email | `{{From Email}}` |
    | sent_datetime | `{{Raw Date}}` |

    ![img](imgs/setup_step_img_15.png)
19. Copy the code [[Click ME](/cloud-versions/zapier.py)] and paste it into the code editor.
20. Input your configuration. [[Click ME](#configuration)]
21. Press the `Continue` button.
22. Press the `Test step` button.
23. If you have configured the Discord webhook URL, you will receive a similar message in your Discord.
![img](imgs/setup_step_img_16.png)

> [!NOTE]\
> The content will be your signal message when TradingView starts sending the signal.

24. Press the `Publish` button.
25. Name your Zap and press the `Turn on Zap` button.

## ⚙️ Configuration
1. `webhook_urls` - Webhook URLs you want to send the alert to. You can add multiple URLs by separating them with a comma.
```python
# Single URL:
webhook_urls = [
    r"https://mywebhook.com/1",
]

# Multi URLs:
webhook_urls = [
    r"https://mywebhook.com/1",
    r"https://mywebhook.com/2",
    r"https://mywebhook.com/3",
    # ...
]
```
> [!NOTE]\
> It is a good idea to test your signal or the program using a webhook test service such as [webhook.site](https://webhook.site/) instead of using your production webhook.

2. Telegram notification
- `tg_bot_token` - Telegram bot token.
- `tg_chat_id` - Telegram chat ID.

3. `discord_webhook_url` - (Optional) Discord webhook URL. Mainly for logging purposes. Leave it blank if you don't want to use it.

