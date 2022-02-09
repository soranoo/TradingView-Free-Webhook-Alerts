# Getting Started with TradingView-Free-Webhook-Alerts

## Installation
- [Installing Python package](#installing-python-package)
- [Setting up configuration](#setting-up-configuration)
- [Setting up email configuration](#setting-up-email-configuration)

## Usage
- [Setting up TradingView alert](#setting-up-tradingview-alert)
- [Program Deployment](#program-deployment)

<a name="installing-python-package"></a>
## 1. Installing the Python package dependencies

To install the Python package dependencies you have to type `pip install -r requirements.txt` into the command prompt which already cd into the project directory.


<a name="setting-up-configuration"></a>
## 2. Setting up configuration

You must finish the following steps before using the program.

1. Make a copy of the [`config.example.toml`](config.example.toml).
2. Rename the copied file to `config.toml`.
3. Open `config.toml` with any text editor you like.
4. Fill in `email_address` and `login_password` with your email and password.
5. Fill in `imap_server` and `imap_port` with your email server and port. (For example, if you are using Gamil, it will be `imap.gmail.com` and `993`.)
6. Fill in `webhook_urls` with your webhook service URLs.
7. Save the config file.

You can adjust other settings on your own.

<a name="setting-up-email-configuration"></a>
## 3. Setting up email configuration

You must finish the following steps before using the program.

1. Enable IMAP in your email account.
2. If you are using Gamil as your email service provider, you have to switch on the "[Less secure apps](https://myaccount.google.com/lesssecureapps)" option.

<a name="setting-up-tradingview-alert"></a>
## 4. Setting up TradingView alert

1. Create a new alert as usual. (Fill in the `Condition`, `Options` and `Expiration time` fields.)
2. Enable `Send email-to-SMS` / `Send email` and other action you want in `Alert actions`. If you want another email address that is different from your TradingView account, you should enable `Send email-to-SMS` instead of `Send email`.
3. Fill in the `Alert name` and your webhook message in `Message`.
4. Save the alert.

![alt text](/docs/imgs/create-tradingview-alert.png)

<a name="program-deployment"></a>
## 5. Program Deployment

1. Run `py main.py` in the command prompt.