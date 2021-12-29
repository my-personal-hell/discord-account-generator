from creator import program
#from discord import discordTokenClient
import random, string
from multiprocessing.dummy import Pool as ThreadPool

def createAccount(a, retries=0):
    try:
        session = program.create(createSession=False)
    except:
        return createAccount(retries+1)
    print(retries, session.token)
    
    with open('tokens.txt', 'a') as f:
        f.write(session.token + '\n')
    

l = list(range(90))
pool = ThreadPool(100)
pool.map(createAccount, l)
