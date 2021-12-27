import requests, time

class captcha:
    def getResult(self):
        response = requests.post('https://api.anti-captcha.com/getTaskResult', json={
            'clientKey': 'a4d26ba7ec33ba9aa810449b42a6d011',
            'taskId': self.taskId
        }).json()
        if response['errorId'] == 0 and response['status'] == 'ready':
            return response['solution']['gRecaptchaResponse']
        return False

    def waitForResult(self):
        while True:
            res = self.getResult()
            if res is not False:
                return res
            time.sleep(3)

    def __init__(self, url, key) -> None:
        response = requests.post('https://api.anti-captcha.com/createTask', json={
            'clientKey': 'a4d26ba7ec33ba9aa810449b42a6d011',
            'task': {
                'type': 'HCaptchaTaskProxyless',
                'websiteURL': url,
                'websiteKey': key
            }
        }).json()

        if (response['errorId'] != 0):
            Exception(response)
        self.taskId = response['taskId']
