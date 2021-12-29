from creator import program
#from discord import discordTokenClient
import random, string
from multiprocessing.dummy import Pool as ThreadPool

# sms-activate: 1658.34 rub
# kopeechka: 1182.70 rub
# anti-captcha: 25.96$

def getProxy():
    ses = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    return "hattorius:IuBYF2gUV38Ydx6D_session-" + ses + "@proxy.packetstream.io:31112"

def createAccount(a, retries=0):
    proxy = getProxy()
    try:
        session = program.create(proxy=proxy, createSession=False)
    except:
        return createAccount(retries+1)
    print(retries, session.token)
    
    with open('tokens.txt', 'a') as f:
        f.write(session.token + '\n')
    

l = list(range(90))
pool = ThreadPool(100)
pool.map(createAccount, l)
