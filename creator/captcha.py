import requests, time

class captcha:
    def getResult(self):
        response = requests.post('https://api.anti-captcha.com/getTaskResult', json={
            'clientKey': self.capthaAPI,
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

    def __init__(self, url, key, capthaAPI) -> None:
        self.capthaAPI = capthaAPI
        response = requests.post('https://api.anti-captcha.com/createTask', json={
            'clientKey': self.capthaAPI,
            'task': {
                'type': 'HCaptchaTaskProxyless',
                'websiteURL': url,
                'websiteKey': key
            }
        }).json()

        if (response['errorId'] != 0):
            Exception(response)
        self.taskId = response['taskId']
