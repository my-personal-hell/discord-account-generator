import requests, time

class email:
    def checkEmail(self):
        response = requests.get('https://api.kopeechka.store/mailbox-get-message?full=1&spa=1&id=' + self.id + '&token=' + self.emailAPI).json()
        return response['value']

    def deleteEmail(self):
        requests.get('https://api.kopeechka.store/mailbox-cancel?id=' + self.id + '&token=' + self.emailAPI)

    def waitForEmail(self):
        tries = 0
        while tries < 30:
            time.sleep(2)
            value = self.checkEmail()
            if value != 'WAIT_LINK':
                self.deleteEmail()
                return value.replace('\\', '')
            tries += 1
        return False

    def __init__(self, emailAPI) -> None:
        self.emailAPI = emailAPI
        response = requests.get('https://api.kopeechka.store/mailbox-get-email?api=2.0&spa=1&site=discord.com&sender=discord&regex=&mail_type=&token=' + self.emailAPI).json()
        if response['status'] == 'OK':
            self.id = response['id']
            self.email = response['mail']
        else:
            Exception(response)
