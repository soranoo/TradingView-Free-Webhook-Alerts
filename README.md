# TradingView-Free-Webhook-Alerts
Project start on 01-02-2022

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GitHub repo size](https://img.shields.io/github/repo-size/soranoo/TradingView-Free-Webhook-Alerts)
![GitHub top language](https://img.shields.io/github/languages/top/soranoo/TradingView-Free-Webhook-Alerts)

Providing the free webhook service to the basic plan users in TradingView.

### Portal ↠ [Installation](docs/gettingstarted.md#installing-python-package) · [Usage](docs/gettingstarted.md#setting-up-tradingview-alert) ↞

## Features
* No Pro/Pro+/Premium TradingView account requested.
  
## How it works ?
Check the inbox frequently and transfer the TradingView alert email into the webhook message.


## Requirements
* Python 3.6 or latest (*Developed in Python 3.8.1)
* An IMAP available email account (eg.Gmail, Hotmail, etc.)
  * Gmail have be tested and works well
* A TradingView account

## Getting Started
To install **TradingView-Free-Webhook-Alerts**, check out the [Getting Started guide](docs/gettingstarted.md).


## Notice
* The program will read the incoming email and mark it as read.
* It is suggested to create a new email account for the best performance.
* If you are using Gmail as your email service provider, you should read through the following documents in order to protect your account from getting suspended; therefore, it is suggested to create a new Google account instead of using your main account.
  * [Gmail receiving limits](https://support.google.com/a/answer/1366776)
  * [Gmail bandwidth limits](https://support.google.com/a/answer/1071518)
  * [Gmail server request limits](https://support.google.com/a/answer/1359240)
* The webhook message will not be sent immediately due to the latency of the email service provider. It will normally take about 2-5 seconds before the webhook message is sent.

## Combination
You can combine the program with other services.
For example,
* You may use [TradingView-Webhook-Bot](https://github.com/fabston/TradingView-Webhook-Bot) to spread the webhook message.
* You may send the webhook to [3commas](https://3commas.io/) for auto trading.

## TODO
* Remove all potential risks that may be caused by the programme, for example, Gmail account was suspended because of high-frequency IMAP action (No reports show any Gmail account has been suspended due to this programme currently.).

## Known Issues
* Inaccurate whole process time ([issue #3](https://github.com/soranoo/TradingView-Free-Webhook-Alerts/issues/3))
* [Rare] Sent duplicate alert ([issue #4](https://github.com/soranoo/TradingView-Free-Webhook-Alerts/issues/4))

## Disclaimer
I as the author assume no responsibility for errors or omissions in the contents of the Service.

In no event shall I be liable for any special, direct, indirect, consequential, or incidental damages or any damages whatsoever, whether in an action of contract, negligence or other torts, arising out of or in connection with the use of the Service or the contents of the Service. I reserve the right to make additions, deletions, or modifications to the contents of the Service at any time without prior notice.

(Service refers to the **TradingView-Free-Webhook-Alerts**.)
