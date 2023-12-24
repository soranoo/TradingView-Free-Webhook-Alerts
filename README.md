# TradingView-Free-Webhook-Alerts
Project start on 01-02-2022


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GitHub repo size](https://img.shields.io/github/repo-size/soranoo/TradingView-Free-Webhook-Alerts)
![GitHub top language](https://img.shields.io/github/languages/top/soranoo/TradingView-Free-Webhook-Alerts)
&nbsp;[![Donation](https://img.shields.io/static/v1?label=Donation&message=❤️&style=social)](https://github.com/soranoo/Donation)

Providing the free webhook service to the basic plan users in TradingView. 

Give me a ⭐ if you like it.

### Portal ↠ [Installation](docs/gettingstarted.md#installing-python-package) · [Usage](docs/gettingstarted.md#setting-up-tradingview-alert) · [Cloud Versions](docs/cloud-versions/cloud-versions.md) · [Videos](https://www.youtube.com/playlist?list=PLOHaKcov3Nkt0LIK1joPYgFnZY24zf_Wo) ↞

## :newspaper: NEWS
###### <<< - 🎄 [Dec 24, 2023] 🎁 - >>>
Added Docker Version ([Read Docs](docs/gettingstarted.md#2-ngrok-version))

###### <<< - [Apr 07, 2023]- >>>
Added [tutorial videos](https://www.youtube.com/playlist?list=PLOHaKcov3Nkt0LIK1joPYgFnZY24zf_Wo)

Config file has been updated. Don't forget to update your existing config file.


## 🗝️ Features
* No Pro/Pro+/Premium TradingView account requested.
* Supported [Dicord](https://discord.com/) monitoring.
  
## 🚩 How it works ?
Listen to the email inbox and transfer the TradingView alert email into the webhook message.


## ⚓ Requirements
* Python 3.8.1 or latest (*Developed in Python 3.8.1 & 3.10.11 & 3.11.6)
* A TradingView account
* See the installation guide for more details.

## 👾 Getting Started
- To install locally or on Docker, check out the [Getting Started guide](docs/gettingstarted.md).
- To install on the cloud, check out the [Cloud Versions](docs/cloud-versions/cloud-versions.md).

##### Comparison - Local vs Docker vs Cloud
| | Local (traditional) | Local (ngrok) | Docker (ngrok) | Cloud |
| --- | --- | --- |--- | --- |
| **Uptime** | Depends on running the environment | Depends on running the environment | Depends on running the environment | 24/7 |
| **Cost** | Free | Free | Free | Free / Paid |
| **Setup** | 💀💀 | 💀💀💀 | 💀💀💀 | 💀 |
| **Limitation** | None? | None? | None? | Depends on the service provider |
| **Speed** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Stability** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Scalability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Portability** | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | N/A |
| **Recommendation** | 🚫 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Tutorial Video** | 🚫 | [Youtube](https://youtu.be/_ZN_rbH1OuM) | 🚫 | [Youtube](https://youtu.be/kTEcJhz0M98) |
| **Setup Docs** | [DOCS](docs/gettingstarted.md#3-traditional-version) | [DOCS](docs/gettingstarted.md#2-ngrok-version) | [DOCS](docs/gettingstarted.md#2-ngrok-version) | [DOCS](docs/cloud-versions/cloud-versions.md) |

> The ngrok Docker version setup is similar to the ngrok local version so I am not going to make a tutorial video for it.

## 📬 Notice
#### Local (traditional)
* The program will read the incoming email and mark it as read.
* It is suggested to create a new email account for the best performance and risk management.
* The webhook message will not be sent immediately due to the latency of the email service provider & TradingView. It will normally take about **2-8 seconds** before the webhook message is sent. (**mainly depends on the network traffic between TradingView and your email service provider**) Please consider carefully before using the program for fast-moving markets.

## 🦔 Potential Risk
#### Local (traditional)
* Email accounts may be locked because of high-frequency IMAP action.
    - Reports have been received that some user was locked by Outlook.

## 🗯️ Combination
You can combine the program with other services.
For example,
* You may use [TradingView-Webhook-Bot](https://github.com/fabston/TradingView-Webhook-Bot) to spread the webhook message.
* You may send a webhook to [3commas](https://3commas.io/) for auto trading.
* You may send a webhook to [Discord](https://discord.com/) for sharing the signal.

## ⭐ TODO
* N/A

## 🐛 Known Issues
* N/A

## 🤖 Useful Links
* Update TradingView `Email-To-SMS`: [LINK](https://www.tradingview.com/support/solutions/43000474398-how-to-change-the-email-to-sms-address-used-for-alert-notifications/)

## 💣 Disclaimer
I as the author assume no responsibility for errors or omissions in the contents of the Service.

In no event shall I be liable for any special, direct, indirect, consequential, or incidental damages or any damages whatsoever, whether in an action of contract, negligence or other torts, arising out of or in connection with the use of the Service or the contents of the Service. I reserve the right to make additions, deletions, or modifications to the contents of the Service at any time without prior notice.

(Service refers to the **TradingView-Free-Webhook-Alerts**.)

## ☕ Donation
Love the program? Consider a donation to support my work.

[!["Donation"](https://raw.githubusercontent.com/soranoo/Donation/main/resources/image/DonateBtn.png)](https://github.com/soranoo/Donation) <- click me~