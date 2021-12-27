
from creator.captcha import captcha
from creator.discord import discord
from creator.email import email
from creator.phone import sms_activate
from creator.utils import generateDOB, generatePassword, generateUsername
import time

class program:
    def __init__(self, proxy=None, username=None) -> None:
        start = time.time()
        accountEmail = email()
        print("Got email ->", accountEmail.email)

        loginCaptcha = captcha('https://discord.com/login', 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34')
        print("Requested captcha solve, task id ->", loginCaptcha.taskId)

        session = discord(proxy)
        print("Discord session created")

        if username is None:
            username = generateUsername()
        password = generatePassword()
        dob = generateDOB()

        print("Waiting for captcha")
        captchaKey = loginCaptcha.waitForResult()

        print("Sending register request")
        session.register(captchaKey, dob, accountEmail.email, password, username)

        print("Performing account check")
        session.check()

        print("Waiting for verification email")
        email_verification_link = accountEmail.waitForEmail()

        emailCaptcha = captcha('https://discord.com/verify', 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34')
        print("Requested captcha solve, task id ->", emailCaptcha.taskId)

        email_verification_token = session.getEmailVerificationToken(email_verification_link)
        print("Received email token")

        print("Waiting for captcha")
        captchaKey = emailCaptcha.waitForResult()

        print("Sending email verification request")
        session.verifyEmail(email_verification_token, captchaKey)

        print("Doing online check")
        if (not session.beOnline()):
            Exception()

        while True:
            print('-')

            smsCaptcha = captcha('https://discord.com/channels/@me', 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34')
            print("Requested captcha Solve, task id ->", smsCaptcha.taskId)

            phone = sms_activate()
            print("Phone number -> +" + phone.number)

            print("Waiting for captcha")
            captchaKey = smsCaptcha.waitForResult()

            print("Requesting SMS from Discord")
            res = session.requestSms(captchaKey, phone.number)

            if res:
                print("Waiting for SMS code")
                smsCode = phone.waitforcode()
                if smsCode is not False:
                    break

            print("Phone verification failed, trying again.")
        print('-')

        print("Received SMS ->", smsCode, "| Submitting to Discord..")
        session.submitSms(smsCode, phone.number)

        print(session.email + ':' + session.password, session.token)
        end = time.time()
        print("Took", round(end-start), "seconds")

