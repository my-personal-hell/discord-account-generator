import random, string

def generatePassword():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

def generateUsername():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(8))

def generateDOB():
    year = str(random.randint(1997,2001))
    month = str(random.randint(1, 12))
    day = str(random.randint(1,28))
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    return year + '-' + month + '-' + day
