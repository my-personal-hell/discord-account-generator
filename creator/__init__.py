
from creator.discord import discord
from creator.email.random import randomEmail
from creator.logging import log
from creator.utils import generateDOB, generatePassword
import time


"""

Verification levels:
0 = unclaimed
1 = non verified
2 = email verified
3 = email & phone verified

"""

class create:
    def __init__(self, username, captchaService=None, emailService=None, proxy=None, verbose=False, token=None, verificationLevel=2) -> None:
        self.token = None

        if verbose:
            log.ok("Creator started")

        self.session = discord(proxy, verbose)
        if verbose:
            log.info("Created Discord session")

        if token is None:
            if not self.session.register(username):
                if verbose:
                    log.warn("Creation without captcha failed, requesting captcha solve")

                if captchaService is None:
                    return

                captchaService.solve("https://discord.com/", "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34")
                if verbose:
                    log.info("Requested captcha, waiting for response")
                captchaToken = captchaService.waitForResult()

                if verbose:
                    log.info("Received captcha token, registering account")
                if not self.session.register(username, captcha_key=captchaToken):
                    return
        else:
            self.session.token = token

        self.token = self.session.token
        if verbose:
            log.ok("Got account, token ->", self.session.token)

        if verificationLevel == 0:
            return

        if verbose:
            log.info("Account going online")

        self.err = True
        def emailVerify():
            log.info("Checking if account is unlocked")
            self.session.isLocked()

            self.birthday = generateDOB()
            self.session.setBirthday(self.birthday)
            if verbose:
                log.info("Set birth day to", self.birthday)

            if emailService is None:
                return
            
            self.email = randomEmail()
            self.password = generatePassword()

            self.session.setEmailAndPassword(self.email.email, self.password)
            if verbose:
                log.info("Requested + set email & set password", [self.email.email, self.password])

            # if verbose:
            #     log.info("Checking if account is unlocked")
            # self.session.isLocked()

            self.err = False

            if verificationLevel == 1:
                return
            
            if verbose:
                log.info("Sleeping for 5 seconds")
            time.sleep(5)

            email = emailService.get()
            self.email = email
            if verbose:
                log.info("Setting real email ->", email.email)
            self.session.setEmailAndPassword(self.email.email, self.password)
            self.session.resendEmail()

        self.session.firstTime()
        self.session.doOnline(emailVerify)

        if verificationLevel == 1 or self.err:
            return

        emailVerificationLink = self.email.waitForEmail()
        if emailVerificationLink is False:
            log.error("Couldn't get verification link in time")
            raise Exception()
        emailVerificationToken = self.session.getEmailVerificationToken(emailVerificationLink)
        if verbose:
            log.info("Email verification token received ->", emailVerificationToken)

        if not self.session.verifyEmail(emailVerificationToken):
            if verbose:
                log.warn("Email verification without captcha failed, requesting captcha solve")

            if captchaService is None:
                return

            captchaService.solve("https://discord.com/verify#token=" + emailVerificationToken, "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34")
            if verbose:
                log.info("Requested captcha, waiting for response")
            captchaToken = captchaService.waitForResult()

            if verbose:
                log.info("Received captcha token, registering account")
            if not self.session.verifyEmail(emailVerificationToken, captcha_key=captchaToken):
                return

            self.token = self.session.token
            log.ok("Email verification completed, new token ->", self.token)
            log.info("Checking if account is unlocked")

            self.session.isLocked()


