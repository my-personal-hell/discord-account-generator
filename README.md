# discord-account-generator
Creates accounts and verifies by email & phone verification. Supports proxies. Uses sms-activate, kopeechka and anti captcha.

**I'm not going to maintain this**

## Table of contents
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installing](#installing)
* [Quick example](#quick-example)
* [License](#license)

## Features
* Uses anti-captcha to solve hcaptcha's
* Uses kopeechka for email's (0.05 rubels per email = 0.00067 USD)
* Uses sms-activate to verify phone numbers (4 - 16 rubels per sms = 0.05 - 0.22 USD)
* Proxy support

## Prerequisites
* [Python 3.9.5](https://www.python.org/downloads/) (did not test on other Python versions)
* [Anti-captcha account](https://anti-captcha.com/) with money on it
* [Kopeechka account](https://kopeechka.store/) with money on it
* [Sms-activate.ru account](https://sms-activate.ru/en/) with even more money on it

Make sure Python is added to your PATH on Windows, more info [here](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path) if you didn't let it set the PATH at install.

## Installing
Please install the requirements:
```
# Linux/macOS
python3 -m pip install -r requirements.txt

# Windows
py -3 -m pip install -r requirements.txt
```
And then you're ready to go

## License
This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.
