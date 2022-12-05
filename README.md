# TradingView-Free-Webhook-Alerts
Project start on 01-02-2022

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GitHub repo size](https://img.shields.io/github/repo-size/soranoo/TradingView-Free-Webhook-Alerts)
![GitHub top language](https://img.shields.io/github/languages/top/soranoo/TradingView-Free-Webhook-Alerts)
&nbsp;[![Donation](https://img.shields.io/static/v1?label=Donation&message=❤️&style=social)](https://github.com/soranoo/Donation)

Providing the free webhook service to the basic plan users in TradingView. Give me a ⭐ if you like it.

### Portal ↠ [Installation](docs/gettingstarted.md#installing-python-package) · [Usage](docs/gettingstarted.md#setting-up-tradingview-alert) · [Cloud Versions](docs/cloud-versions/cloud-versions.md)↞

## :newspaper: NEWS
###### <<< - [Dec 05, 2022]- >>>
[pipedream](https://pipedream.com/) version is now available! [[Read More](/docs/cloud-versions/pipedream/pipedream.md#shortcuts)]
###### <<< - [Oct 06, 2022]- >>>
Gmail is back! Please follow the [instruction](docs/gettingstarted.md#setting-up-gmail-configuration) if you want to switch to Gmail.

###### <<< - [Aug 26, 2022]- >>>
Removed TradingView `Send email` support temporarily. Please use `Send email-to-SMS` instead.

## 🗝️ Features
* No Pro/Pro+/Premium TradingView account requested.
  
## 🚩 How it works ?
Listen to the email inbox and transfer the TradingView alert email into the webhook message.


## ⚓ Requirements
* Python 3.6 or latest (*Developed in Python 3.8.1)
* An IMAP available email account (eg.Hotmail, Outlook, Gmail, etc.)
  * Hotmail&Gmail have be tested and works well.
* A TradingView account

## 👾 Getting Started
- To install locally, check out the [Getting Started guide](docs/gettingstarted.md).
- To install on the cloud, check out the [Cloud Versions](docs/cloud-versions/cloud-versions.md).

##### Comparison - Local vs Cloud
| | Local | Cloud |
| --- | --- | --- |
| **Runtime** | When your computer is on | 24/7 |
| **Cost** | Free | Free / Paid |
| **Setup** | Easy? | Easy |
| **Log** | Full Log | Depends on the service provider |
| **Limitation** | None? | Depends on the service provider |
| **Scalability** | ⭐Unlimited🌟 | Depends on the service provider |
| **Setup Docs** | [DOCS](docs/gettingstarted.md) | [DOCS](docs/cloud-versions/cloud-versions.md) |


## 📬 Notice
* The program will read the incoming email and mark it as read.
* It is suggested to create a new email account for the best performance and risk management.
* The webhook message will not be sent immediately due to the latency of the email service provider & TradingView. It will normally take about **2-8 seconds** before the webhook message is sent. (**mainly depends on the network traffic between TradingView and your email service provider**) Please consider carefully before using the program for fast-moving markets.

## 🗯️ Combination
You can combine the program with other services.
For example,
* You may use [TradingView-Webhook-Bot](https://github.com/fabston/TradingView-Webhook-Bot) to spread the webhook message.
* You may send a webhook to [3commas](https://3commas.io/) for auto trading.
* You may send a webhook to [Discord](https://discord.com/) for sharing the signal.

## ⭐ TODO
* Remove all potential risks that may be caused by the program, for example, Outlook account was locked because of high-frequency IMAP action.

## 🐛 Known Issues
* N/A

## 🤖 Useful Links
* Update TradingView `Email-To-SMS`: [LINK](https://www.tradingview.com/support/solutions/43000474398-how-to-change-the-email-to-sms-address-used-for-alert-notifications/)

## 💣 Disclaimer
I as the author assume no responsibility for errors or omissions in the contents of the Service.

In no event shall I be liable for any special, direct, indirect, consequential, or incidental damages or any damages whatsoever, whether in an action of contract, negligence or other torts, arising out of or in connection with the use of the Service or the contents of the Service. I reserve the right to make additions, deletions, or modifications to the contents of the Service at any time without prior notice.

(Service refers to the **TradingView-Free-Webhook-Alerts**.)

## ☕ Donation
Love the program? Consider a donation to support our work.

[!["Donation"](https://raw.githubusercontent.com/soranoo/Donation/main/resources/image/DonateBtn.png)](https://github.com/soranoo/Donation) <- click me~