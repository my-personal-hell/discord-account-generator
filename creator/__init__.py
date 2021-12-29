
from creator.captcha import captcha
from creator.discord import discord
from creator.email import email
from creator.phone import sms_activate
from creator.utils import generateDOB, generatePassword, generateUsername
import time

def create(capthaAPI, emailAPI, phoneAPI, proxy=None, username=None, verbose:bool=False):
    start = time.time()
    accountEmail = email(emailAPI)
    if verbose:
        print("Got email ->", accountEmail.email)

    loginCaptcha = captcha('https://discord.com/login', 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34', capthaAPI)
    if verbose:
        print("Requested captcha solve, task id ->", loginCaptcha.taskId)

    session = discord(proxy, verbose)
    if verbose:
        print("Discord session created")

    if username is None:
        username = generateUsername()
    password = generatePassword()
    dob = generateDOB()

    if verbose:
        print("Waiting for captcha")
    captchaKey = loginCaptcha.waitForResult()

    if verbose:
        print("Sending register request")
    session.register(captchaKey, dob, accountEmail.email, password, username)

    if verbose:
        print("Performing account check")
    session.check()

    if verbose:
        print("Waiting for verification email")
    email_verification_link = accountEmail.waitForEmail()

    emailCaptcha = captcha('https://discord.com/verify', 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34', capthaAPI)
    if verbose:
        print("Requested captcha solve, task id ->", emailCaptcha.taskId)

    email_verification_token = session.getEmailVerificationToken(email_verification_link)
    if verbose:
        print("Received email token")

    if verbose:
        print("Waiting for captcha")
    captchaKey = emailCaptcha.waitForResult()

    if verbose:
        print("Sending email verification request")
    session.verifyEmail(email_verification_token, captchaKey)

    if verbose:
        print("Performing online check")
    if (not session.beOnline()):
        Exception()

    while True:
        if verbose:
            print('-')

        smsCaptcha = captcha('https://discord.com/channels/@me', 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34', capthaAPI)
        if verbose:
            print("Requested captcha Solve, task id ->", smsCaptcha.taskId)

        phone = sms_activate(phoneAPI)
        if verbose:
            print("Phone number -> +" + phone.number)

        if verbose:
            print("Waiting for captcha")
        captchaKey = smsCaptcha.waitForResult()

        if verbose:
            print("Requesting SMS from Discord")
        res = session.requestSms(captchaKey, phone.number)

        if res:
            if verbose:
                print("Waiting for SMS code")
            smsCode = phone.waitforcode()
            if smsCode is not False:
                break
            
        if verbose:
            print("Phone verification failed, trying again.")
    if verbose:
        print('-')

    if verbose:
        print("Received SMS ->", smsCode, "| Submitting to Discord..")
    session.submitSms(smsCode, phone.number)
        
    if verbose:
        print("Performing account check")
    session.check()

    end = time.time()
    if verbose:
        print("Took", round(end-start), "seconds")
            
    if verbose:
        print(session.email + ":" + session.password + " - " + session.token)

    return session
