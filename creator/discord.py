import requests, json, discum
from base64 import b64encode as b
from discord_build_info_py import *

class discord:
    def createSession(self, proxy) -> bool:
        self.session = requests.Session()
        build_num, build_hash, build_id = getClientData('stable')
        self.build_num = build_num
        self.proxy = proxy
        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'

        if proxy is not None:
            self.session.proxies.update({'http': 'http://' + proxy, 'https': 'http://' + proxy}) # ip:port OR user:pass@ip:port
            try:
                self.session.get('https://ipv4.icanhazip.com/').text
            except:
                return False

        try:
            response = self.session.get('https://discord.com/register')
        except:
            return False
        self.dcfduid = response.headers['Set-Cookie'].split('__dcfduid=')[1].split(';')[0]
        self.session.cookies['__dcfduid'] = self.dcfduid
        self.sdcfduid = response.headers['Set-Cookie'].split('__sdcfduid=')[1].split(';')[0]
        self.session.cookies['__sdcfduid'] = self.sdcfduid
        self.session.cookies['locale'] = 'en'

        self.super_properties = b(json.dumps({
            "os": "Windows",
            "browser": "Firefox",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": self.useragent,
            "browser_version": "90.0",
            "os_version": "10",
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

    def getFingerPrint(self):
        response = self.session.get('https://discord.com/api/v9/experiments').json()
        self.fingerprint = response['fingerprint']
        self.session.headers.update({'x-fingerprint': response['fingerprint']})

    def tryRegister(self, date_of_birth):
        self.session.post('https://discord.com/api/v9/auth/register', headers={
            'referer': 'https://discord.com/register',
            'authorization': 'undefined'
        }, json={
            'captcha_key': None,
            'consent': True,
            'date_of_birth': date_of_birth,
            'email': self.email,
            'fingerprint': self.fingerprint,
            'gift_code_sku_id': None,
            'invite': None,
            'password': self.password,
            'username': self.username
        })

    def register(self, captcha_key, date_of_birth, email, password, username):
        self.email = email
        self.password = password
        self.username = username
        self.tryRegister(date_of_birth)
        response = self.session.post('https://discord.com/api/v9/auth/register', headers={
            'referer': 'https://discord.com/register',
            'authorization': 'undefined'
        }, json={
            'captcha_key': captcha_key,
            'consent': True,
            'date_of_birth': date_of_birth,
            'email': email,
            'fingerprint': self.fingerprint,
            'gift_code_sku_id': None,
            'invite': None,
            'password': password,
            'username': username
        }).json()
        if self.verbose:
            print(response)
        self.token = response['token']
        
    def check(self):
        check = self.session.patch('https://discord.com/api/v9/users/@me/library', headers={
            "authorization": self.token,
            'Referer': 'https://discord.com/channels/@me',
            "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Firefox\";v=\"91\", \"Chromium\";v=\"91\"",
            "sec-ch-ua-mobile": "?0"
        })
        if check.status_code == 403:
            Exception("Token locked!")
        elif check.status_code == 400:
            Exception(check)
            
    def getEmailVerificationToken(self, link):
        return self.session.get(link).url.split('#token=')[1]

    def verifyEmail(self, token, captcha_key):
        response = self.session.post('https://discord.com/api/v9/auth/verify', headers={
            "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Firefox\";v=\"91\", \"Chromium\";v=\"91\"",
            'referer': 'https://discord.com/verify',
            'authorization': self.token
        }, json={
            'captcha_key': captcha_key,
            'token': token
        }).json()
        if self.verbose:
            print(response)
        self.token = response['token']

    def beOnline(self):
        try:
            if self.verbose and self.proxy is not None:
                print(self.proxy)
            if self.proxy is not None:
                bot = discum.Client(token=self.token, log=False, user_agent=self.useragent, build_num=self.build_num, 
                        proxy='http://' + self.proxy)
            else:
                bot = discum.Client(token=self.token, log=False, user_agent=self.useragent, build_num=self.build_num)
            @bot.gateway.command
            def websocket_activate(resp):
                if resp.event.ready_supplemental:
                    bot.gateway.close()
            bot.gateway.run()
        except Exception as e:
            print(e)
            return False
        return True

    def requestSms(self, captcha_key, number):
        response = self.session.post('https://discord.com/api/v9/users/@me/phone', headers={'referer': 'https://discord.com/channels/@me', 'authorization': self.token}, json={
            'captcha_key': captcha_key,
            'change_phone_reason': 'user_action_required',
            'phone': '+' + number
        })
        if response.status_code == 204:
            return True
        if self.verbose:
            print(response.text)
        return False

    def submitSms(self, code, number):
        token = self.session.post('https://discord.com/api/v9/phone-verifications/verify', headers={'referer': 'https://discord.com/channels/@me', 'authorization': self.token}, json={
            'code': code,
            'phone': '+' + number
        }).json()
        if self.verbose:
            print(token)
        token = token['token']
        response = self.session.post('https://discord.com/api/v9/users/@me/phone', headers={'referer': 'https://discord.com/channels/@me', 'authorization': self.token}, json={
            'change_phone_reason': 'user_action_required',
            'password': self.password,
            'phone_token': token
        })
        if self.verbose:
            print(response.status_code)
        if response.status_code != 204:
            Exception("Something went wrong with SMS verification")

    def __init__(self, proxy, verbose) -> None:
        self.proxy = proxy
        self.verbose = verbose
        if (not self.createSession(proxy)):
            Exception('Something went wrong with proxy!')
        self.getFingerPrint()
