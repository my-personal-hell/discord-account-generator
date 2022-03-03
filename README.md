# not working anymore

## STILL WORKING OF JANUARY THE 19TH 2022
![image](https://user-images.githubusercontent.com/54858358/147946093-760185d3-171a-4e4a-b907-34fdc44652cd.png)
(just tested it)

# discord-account-generator
Creates accounts and verifies by email & phone verification. Supports proxies. Uses sms-activate, kopeechka and anti captcha.

**I'm not going to maintain this**

## Table of contents
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installing](#installing)
* [Quick example](#quick-example)
* [License](#license)
* [Donate](#donate)
* [About me](#about-me)

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

## Quick Example
### Create token
```py
from creator import create

anticaptcha = 'a4d26ba7ec33ba9aa810449b42a6d011'
kopeechka = '99355de805609eac0dc5750f49fb18e5'
smsactivate = 'b97683d5f482A06051Ab7fc81bb4d495'

create(capthaAPI=anticaptcha,
       emailAPI=kopeechka,
       phoneAPI=smsactivate,
       verbose=True)
```

### Create token and continue with program with custom username
```py
from creator import create

anticaptcha = 'a4d26ba7ec33ba9aa810449b42a6d011'
kopeechka = '99355de805609eac0dc5750f49fb18e5'
smsactivate = 'b97683d5f482A06051Ab7fc81bb4d495'

session = create(capthaAPI=anticaptcha,
       emailAPI=kopeechka,
       phoneAPI=smsactivate,
       username="Hatty was here")
       
token = session.token
# continue, do whatever you want
```

### Simple multithreading with proxies
```py
from multiprocessing.dummy import Pool as ThreadPool
from creator import create
import random

anticaptcha = 'a4d26ba7ec33ba9aa810449b42a6d011'
kopeechka = '99355de805609eac0dc5750f49fb18e5'
smsactivate = 'b97683d5f482A06051Ab7fc81bb4d495'
createAmount = 100

proxies = ["ip:port", "user:password@ip:port"]

def createAccount(a, retries=0):
    try:
        session = create(capthaAPI=anticaptcha,
                         emailAPI=kopeechka,
                         phoneAPI=smsactivate,
                         proxy=proxies[random.randint(0, len(proxies)-1)])
    except:
        return createAccount(a, retries + 1)
        
    with open('tokens.txt', 'a+') as f:
        f.write(session.token + '\n')

pool = ThreadPool(100)
pool.map(createAccount, list(range(createAmount)))
```

## License
This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.

## Donate
ETH: `hattywashere.eth`
that's pretty much it.

## About me
You can read all about me with contact information [at my website](https://xlogic.sh).
