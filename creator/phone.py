import requests, time

class sms_activate:
    def get_code(self):
        response = requests.get('https://api.sms-activate.org/stubs/handler_api.php?api_key=' + self.phoneAPI + '&action=getStatus&id=' + self.id).text
        if 'STATUS_OK' not in response:
            return False
        return response.split(':')[1]

    def sent(self) -> None:
        requests.get('https://api.sms-activate.org/stubs/handler_api.php?api_key=' + self.phoneAPI + '&action=setStatus&status=1&id=' + self.id)

    def done(self) -> None:
        requests.get('https://api.sms-activate.org/stubs/handler_api.php?api_key=' + self.phoneAPI + '&action=setStatus&status=6&id=' + self.id)

    def banned(self) -> None:
        requests.get('https://api.sms-activate.org/stubs/handler_api.php?api_key=' + self.phoneAPI + '&action=setStatus&status=8&id=' + self.id)

    def waitforcode(self):
        self.sent()
        tries = 0
        while tries < 30:
            time.sleep(3)
            res = self.get_code()
            if res is not False:
                self.done()
                return res
            tries += 1
        self.banned()
        return False


    def __init__(self, phoneAPI) -> None:
        self.phoneAPI = phoneAPI
        response = requests.get('https://api.sms-activate.org/stubs/handler_api.php?api_key=' + self.phoneAPI + '&action=getNumber&service=ds&ref=1715152&country=43').text
        if ":" not in response:
            Exception(response)
        self.id = response.split(':')[1]
        self.number = response.split(':')[2]
        pass
