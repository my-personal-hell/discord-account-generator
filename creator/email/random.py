import random, string

def generateRandomEmail():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12)) + '@' + ''.join(random.choice(string.ascii_uppercase) for _ in range(8)) + '.' + ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

class randomEmail:
    def __init__(self):
        self.email = generateRandomEmail()
