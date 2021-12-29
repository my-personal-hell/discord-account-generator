import requests, json, urllib, discum, time, random
from creator.discord import discord
from discord_build_info_py import *
from base64 import b64encode as b

def ue(input):
    return urllib.parse.quote(input)

class discordTokenClient:
    api = 'https://discord.com/api/'
    
    def getUserInfo(self, userid):
        response = self.GETapi('v9/users/' + str(userid) + '/profile?with_mutual_guilds=false', 
                               referer="https://discord.com/channels/@me").json()
        return response
    
    def createDMChannel(self, memberid):
        response = self.POSTapi('v9/users/@me/channels', payload={'recipients': [str(memberid)]}, referer="https://discord.com/channels/@me").json()
        print(response)
        return int(response['id'])
    
    def sendDMMessage(self, channelid, content):
        nonce = str(time.time() - 1420070400 + 705000000).replace('.','')  + str(random.randrange(10, 99))
        response = self.POSTapi('v9/channels/' + str(channelid) + '/messages', payload={'content': content, 'nonce': nonce, 'tts': False}, 
                                referer="https://discord.com/channels/@me/" + str(channelid))
        print(response.status_code)
        print(response.json())
    
    def getOnlineMembers(self, guildid, channelid):
        guildid = str(guildid)
        channelid = str(channelid)
        
        if self.proxy is not None:
            bot = discum.Client(token=self.token, log=False, user_agent=self.useragent, build_num=self.build_num, 
                                proxy='http://' + self.proxy)
        else:
            bot = discum.Client(token=self.token, log=False, user_agent=self.useragent, build_num=self.build_num)
        
        def closeAfterFetching(response, guildid):
            if bot.gateway.finishedMemberFetching(guildid):
                bot.gateway.removeCommand({'function': closeAfterFetching, 'params': {'guildid': guildid}})
                bot.gateway.close()
        
        bot.gateway.fetchMembers(guildid, channelid, keep='all', wait=1)
        bot.gateway.command({'function': closeAfterFetching, 'params': {'guildid': guildid}})
        bot.gateway.run()
        bot.gateway.resetSession()
        
        memberList = bot.gateway.session.guild(guildid).members
        memberIds = []
        for memberid in memberList:
            memberIds.append(memberid)
            
        return memberIds
    
    def beOnline(self):
        try:
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
    
    def getInvite(self, invite):
        response = self.GETapi('v9/invites/' + invite, {'inputValue': invite, 'with_counts': True, 'with_expiration': False}).json()
        try:
            return {
                'valid': True,
                'members': response['approximate_member_count'],
                'online': response['approximate_presence_count']
            }
        except:
            return {'valid': False}
    
    def joinInvite(self, invite):
        response = self.POSTapi('v9/invites/' + invite, payload={}).json()
        print(response)
        if response['new_member']:
            return True
        return False
    
    def getChannelMessages(self, channelid):
        response = self.GETapi('v9/channels/' + str(channelid) + '/messages?limit=50').json()
        return response
    
    def findVerificationMessage(self, channelid, messageid):
        messages = self.getChannelMessages(channelid)
        print(messages)
        for message in messages:
            print("if", message['id'], '==', messageid)
            if int(message['id']) == int(messageid):
                return message
        return False
    
    def addReaction(self, message=None, channelid=None, messageid=None, emoji=None):
        if message is not None:
            channelid = message['channel_id']
            messageid = message['id']
            emoji = message['reactions'][0]['emoji']['name']
        response = self.session.put('https://discord.com/api/v9/channels/' + str(channelid) + '/messages/' + str(messageid) + '/reactions/' + ue(emoji) + '/' + ue('@me'))
        if response.status_code == 204:
            return True
        return False
    
    def GETapi(self, url, payload:dict=None, referer:str=None):
        url = self.api + url
        return self.session.get(url, params=payload, headers={'referer': referer} if referer is not None else {})
    
    def POSTapi(self, url, payload:dict=None, referer:str=None):
        url = self.api + url
        return self.session.post(url, json=payload, headers={'referer': referer} if referer is not None else {})
    
    def check(self):
        check = self.session.patch('https://discord.com/api/v9/users/@me', json={
            'email': self.email,
            'password': self.password
        })
        if check.status_code == 403:
            Exception("Token locked!")
        elif check.status_code == 400:
            Exception(check)
    
    def getCfCookies(self):
        response = self.session.get('https://discord.com/app')
        dcfduid = response.headers['Set-Cookie'].split('__dcfduid=')[1].split(';')[0]
        sdcfduid = response.headers['Set-Cookie'].split('__sdcfduid=')[1].split(';')[0]
        return [dcfduid, sdcfduid]
    
    def getFingerprint(self):
        response = self.session.get('https://discord.com/api/v9/experiments').json()
        return response['fingerprint']
    
    def createSession(self, super_properties, fingerprint, build_num, proxy, useragent):
        self.session = requests.Session()
        
        # proxy
        self.proxy = proxy
        if self.proxy is not None:
            self.session.proxies.update({'http': 'http://' + proxy, 'https': 'http://' + proxy}) # ip:port OR user:pass@ip:port
            try:
                self.session.get('https://ipv4.icanhazip.com/').text
            except:
                Exception("Could not connect to proxy!")
        
        # cloudflare cookies
        self.dcfduid, self.sdcfduid = self.getCfCookies()
        
        # x-fingerprint
        if fingerprint is not None:
            self.fingerprint = fingerprint
        else:
            self.fingerprint = self.getFingerprint()
            
        # build number
        if build_num is not None:
            self.build_num = build_num
        else:
            self.build_num = getClientData('stable')[0]
            
        # user agent
        if useragent is not None:
            self.useragent = useragent
        else:
            self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
            
        # super properties
        if super_properties is not None:
            self.super_properties = super_properties
        else:
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
                "client_build_number": int(self.build_num),
                "client_event_source": None
            }, separators=(',', ':')).encode()).decode()
            
        # set cookies
        self.session.cookies['__dcfduid'] = self.dcfduid
        self.session.cookies['__sdcfduid'] = self.sdcfduid
        self.session.cookies['locale'] = 'en'
        
        # set headers
        self.session.headers.update({
            'Accept': '*/*',
            'Accept-Language': 'en',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Content-Type': 'application/json',
            'Origin': 'https://discord.com/',
            'Referer': 'https://discord.com/channels/@me',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': self.useragent,
            'X-Super-Properties': self.super_properties,
            'Cookie': '__dcfduid=' + self.dcfduid + '; __sdcfduid=' + self.sdcfduid,
            'TE': 'Trailers',
            'authorization': self.token,
            "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Firefox\";v=\"91\", \"Chromium\";v=\"91\"",
            "sec-ch-ua-mobile": "?0",
            'x-fingerprint': self.fingerprint,
            'x-discord-locale': 'en-US'
        })
    
    def __init__(self, token, session=None, super_properties=None, fingerprint=None, build_num=None, proxy=None, useragent=None) -> None:
        self.token = token
        print("Received token: " + self.token)
        
        if session is not None:
            self.session = session
            self.fingerprint = self.getFingerprint()
            self.session.headers.update({
                'x-discord-locale': 'en-US',
                'authorization': self.token,
                "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Firefox\";v=\"91\", \"Chromium\";v=\"91\"",
                "sec-ch-ua-mobile": "?0",
                'x-fingerprint': self.fingerprint,
                'x-discord-locale': 'en-US'
            })
        else:
            self.createSession(super_properties, fingerprint, build_num, proxy, useragent)
            pass

def discordClient(discord: discord):
    tokenClient = discordTokenClient(
        discord.token,
        session=discord.session
    )
    return tokenClient
        
