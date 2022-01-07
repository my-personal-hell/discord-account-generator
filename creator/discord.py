import requests, json, discum
from creator.logging import log
from base64 import b64encode as b
from discord_build_info_py import *

class discord:
    def createSession(self):
        self.session = requests.Session()
        build_num, build_hash, build_id = getClientData('stable')
        self.build_num = build_num
        self.useragent = 'ozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'

        if self.proxy is not None:
            self.session.proxies.update({'http': 'http://' + self.proxy, 'https': 'http://' + self.proxy}) # ip:port OR user:pass@ip:port

        try:
            response = self.session.get('https://discord.com/register')
        except:
            return False

        self.dcfduid = response.headers['Set-Cookie'].split('__dcfduid=')[1].split(';')[0]
        self.session.cookies['__dcfduid'] = self.dcfduid
        self.sdcfduid = response.headers['Set-Cookie'].split('__sdcfduid=')[1].split(';')[0]
        self.session.cookies['__sdcfduid'] = self.sdcfduid
        self.session.cookies['locale'] = 'en-US'
        self.session.cookies['OptanonConsent'] = 'isIABGlobal=false&datestamp=Thu+Jan+06+2022+19%3A32%3A45+GMT%2B0100+(Central+European+Standard+Time)&version=6.17.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F'

        if self.verbose:
            log.info("Dcfduid ->", self.dcfduid)
            log.info("Sdcfduid ->", self.sdcfduid)

        self.super_properties = b(json.dumps({
            "os": "Linux",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": self.useragent,
            "browser_version": "96.0.4664.110",
            "os_version": "",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": int(build_num),
            "client_event_source": None
        }, separators=(',', ':')).encode()).decode()

        self.session.headers.update({
            'Accept': '*/*',
            'Accept-Language': 'en',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Content-Type': 'application/json',
            'Origin': 'https://discord.com/',
            'Referer': 'https://discord.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': self.useragent,
            'X-Super-Properties': self.super_properties,
            'Cookie': '__dcfduid=' + self.dcfduid + '; __sdcfduid=' + self.sdcfduid,
            'TE': 'Trailers'
        })

        return True

    def getFingerprint(self):
        response = self.session.get('https://discord.com/api/v9/experiments', headers={
            'x-track': self.super_properties
        })
        self.fingerprint = response.json()['fingerprint']
        if self.verbose:
            log.info("Fingerprint ->", self.fingerprint)
        return self.fingerprint

    def register(self, username, captcha_key=None):
        payload = {
            'consent': True,
            'fingerprint': self.fingerprint,
            'username': username
        }
        if captcha_key is not None:
            payload['captcha_key'] = captcha_key

        response = self.session.post('https://discord.com/api/v9/auth/register', json=payload)
        if response.status_code == 201:
            self.token = response.json()['token']
            return True
        return False

    def firstTime(self):
        self.session.get('https://discord.com/welcome/', headers={
            "authorization": self.token
        })
        pass

    def doOnline(self, cb):
        if self.proxy is not None:
            bot = discum.Client(token=self.token, log=False, user_agent=self.useragent, build_num=self.build_num, proxy='http://' + self.proxy)
        else:
            bot = discum.Client(token=self.token, log=False, user_agent=self.useragent, build_num=self.build_num)
        @bot.gateway.command
        def websocket_activate(resp):
            if resp.event.ready_supplemental:
                cb()
                bot.gateway.close()
        bot.gateway.run()

    def setBirthday(self, birthday):
        response = self.session.patch("https://discord.com/api/v9/users/@me", json={
            'date_of_birth': birthday
        }, headers={
            'Referer': 'https://discord.com/channels/@me',
            "authorization": self.token # facepalm
        })
        if response.status_code == 200:
            return True
        return False

    def setEmailAndPassword(self, email, password):
        response = self.session.patch("https://discord.com/api/v9/users/@me", json={
            'email': email,
            'password': password
        }, headers={
            'Referer': 'https://discord.com/channels/@me',
            "authorization": self.token
        })
        if response.status_code == 200:
            return True
        return False

    def getEmailVerificationToken(self, link):
        return self.session.get(link).url.split('#token=')[1]

    def verifyEmail(self, token, captcha_key=None):
        response = self.session.post('https://discord.com/api/v9/auth/verify', headers={
            "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Firefox\";v=\"91\", \"Chromium\";v=\"91\"",
            'referer': 'https://discord.com/verify',
            'authorization': self.token
        }, json={
            'captcha_key': captcha_key,
            'token': token
        })
        if response.status_code == 400:
            return False
        response = response.json()
        if self.verbose:
            log.ok("Email verification successful, token ->", response['token'])
        self.token = response['token']
        return True

    def __init__(self, proxy, verbose) -> None:
        self.proxy = proxy
        self.verbose = verbose
        if not self.createSession():
            raise Exception("Failed creating Discord session")
        self.getFingerprint()
