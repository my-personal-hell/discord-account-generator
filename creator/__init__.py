
from creator.discord import discord
from creator.logging import log
from creator.utils import generateDOB, generatePassword


"""

Verification levels:
0 = non verified
1 = email verified
2 = email & phone verified

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

        def emailVerify():
            self.birthday = generateDOB()
            self.session.setBirthday(self.birthday)
            if verbose:
                log.info("Set birth day to", self.birthday)

            if emailService is None:
                return
            
            email = emailService.get()
            self.email = email.email
            self.password = generatePassword()

            self.session.setEmailAndPassword(self.email, self.password)
            if verbose:
                log.info("Requested email & set password", [self.email, self.password])

            emailVerificationLink = email.waitForEmail()
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
                self.ok("Email verification completed ->", self.token)
            


        self.session.firstTime()
        self.session.doOnline(emailVerify)


