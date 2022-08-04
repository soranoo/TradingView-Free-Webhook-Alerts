# TradingView-Free-Webhook-Alerts
Project start on 01-02-2022

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GitHub repo size](https://img.shields.io/github/repo-size/soranoo/TradingView-Free-Webhook-Alerts)
![GitHub top language](https://img.shields.io/github/languages/top/soranoo/TradingView-Free-Webhook-Alerts)

Providing the free webhook service to the basic plan users in TradingView.

### Portal ↠ [Installation](docs/gettingstarted.md#installing-python-package) · [Usage](docs/gettingstarted.md#setting-up-tradingview-alert) ↞

## :newspaper: NEWS
:warning: **Gmail** is not longer SUPPORTED :warning:

**Google** has removed `Less secure apps` option. ([Reference Article](https://support.google.com/accounts/answer/6010255))
```
To help keep your account secure, from May 30, 2022,
​​Google no longer supports the use of third-party apps or
devices which ask you to sign in to your Google Account
using only your username and password.

Important: This deadline does not apply to Google Workspace or
Google Cloud Identity customers. The enforcement date for these
customers will be announced on the Workspace blog at a later date.

(BY Google)
```
(Special thanks: [`Pest202`](https://github.com/soranoo/TradingView-Free-Webhook-Alerts/issues/3))

For those who are seeking an alternative to Gmail: [LINK](https://github.com/soranoo/TradingView-Free-Webhook-Alerts/issues/5#issuecomment-1205433464)

:information_source: I will keep looking for other better IMAP services.
Please feel free to contact me if you have any suggestions.


## :old_key: Features
* No Pro/Pro+/Premium TradingView account requested.
  
## :triangular_flag_on_post: How it works ?
Check the inbox frequently and transfer the TradingView alert email into the webhook message.


## :anchor: Requirements
* Python 3.6 or latest (*Developed in Python 3.8.1)
* An IMAP available email account (eg.Hotmail, Outlook, etc.)
  * Hotmail have be tested and works well
* A TradingView account

## :space_invader: Getting Started
To install **TradingView-Free-Webhook-Alerts**, check out the [Getting Started guide](docs/gettingstarted.md).


## :mailbox_with_mail: Notice
* The program will read the incoming email and mark it as read.
* It is suggested to create a new email account for the best performance.
* The webhook message will not be sent immediately due to the latency of the email service provider. It will normally take about 2-5 seconds before the webhook message is sent.

## :right_anger_bubble: Combination
You can combine the program with other services.
For example,
* You may use [TradingView-Webhook-Bot](https://github.com/fabston/TradingView-Webhook-Bot) to spread the webhook message.
* You may send the webhook to [3commas](https://3commas.io/) for auto trading.

## :star: TODO
* Remove all potential risks that may be caused by the programme, for example, Gmail account was suspended because of high-frequency IMAP action (No reports show any Gmail account has been suspended due to this programme currently.).

## :bug: Known Issues
* Inaccurate whole process time ([issue #3](https://github.com/soranoo/TradingView-Free-Webhook-Alerts/issues/3))
* [Rare] Sent duplicate alert ([issue #4](https://github.com/soranoo/TradingView-Free-Webhook-Alerts/issues/4))

## :robot: Useful Links
* Update TradingView `Email-To-SMS`: [LINK](https://www.tradingview.com/support/solutions/43000474398-how-to-change-the-email-to-sms-address-used-for-alert-notifications/)

## :bomb: Disclaimer
I as the author assume no responsibility for errors or omissions in the contents of the Service.

In no event shall I be liable for any special, direct, indirect, consequential, or incidental damages or any damages whatsoever, whether in an action of contract, negligence or other torts, arising out of or in connection with the use of the Service or the contents of the Service. I reserve the right to make additions, deletions, or modifications to the contents of the Service at any time without prior notice.

(Service refers to the **TradingView-Free-Webhook-Alerts**.)
