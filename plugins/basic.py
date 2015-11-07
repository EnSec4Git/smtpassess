__author__ = 'Yavor-Nb'

import smtplib, time

FAKE_HOSTNAME = "gmail.com"

class BasicTester:
    def __init__(self, logger, configuration):
        self.logger = logger
        self.results = []
        self.timeout = 5
        if configuration.has_option("general", "test_timeout"):
            self.timeout = configuration.get("general", "test_timeout")
        self.valid_mail = configuration.get("target", "valid_email")

    def perform_tests(self, target):
        # Test 1: Check if server accepts its own hostname
        smtpobj = smtplib.SMTP(target[0], target[1], target[0])
        try:
            smtpobj.helo()
            self.results.append(False)
        except:
            self.results.append(True)

        time.sleep(self.timeout)

        # Test 2: Check if server accepts fake hostname
        smtpobj = smtplib.SMTP(target[0], target[1], FAKE_HOSTNAME)
        try:
            smtpobj.helo()
            self.results.append(False)
        except:
            self.results.append(True)

        time.sleep(self.timeout)

        # Test 3: Check if server will verify email address
        smtpobj = smtplib.SMTP(target[0], target[1])
        try:
            smtpobj.helo()
            res = smtpobj.verify(self.valid_mail)
            if res[0] != 250:
                raise Exception("not verified")
            self.results.append(False)
        except:
            self.results.append(True)

        time.sleep(self.timeout)

    def check_results(self, mail_access):
        if not self.results[0]:
            self.logger.log(2, "Server accepted its own hostname")
        else:
            self.logger.log(1, "Server rejected its own hostname")

        if not self.results[1]:
            self.logger.log(2, "Server accepted HELO from a fake hostname")
        else:
            self.logger.log(1, "Server refused HELO from a fake hostname")

        if not self.results[2]:
            self.logger.log(3, "Server verified email")
        else:
            self.logger.log(1, "Server refused to verify email")

tester = BasicTester