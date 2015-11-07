__author__ = 'Yavor-Nb'

import smtplib
import time

class SslTester:
    def __init__(self, logger, configuration):
        self.logger = logger
        self.timeout = 5
        self.results = []
        if configuration.has_option("general", "test_timeout"):
            self.timeout = configuration.get("general", "test_timeout")

    def perform_tests(self, target):
        # Test 1: Try to connect through standard SSL port
        try:
            smtpobj = smtplib.SMTP_SSL(target[0], 465)
            smtpobj.helo()
            self.results.append(True)
        except:
            self.results.append(False)

        time.sleep(self.timeout)

        # Test 2: Test STARTTLS support
        smtpobj = smtplib.SMTP(target[0], target[1])
        try:
            smtpobj.helo()
            smtpobj.starttls()
            self.results.append(True)
        except:
            self.results.append(False)

        time.sleep(self.timeout)

    def check_results(self, mail_access):
        if self.results[0]:
            self.logger.log(1, "Server accepts SSL connections at port 465")
        else:
            self.logger.log(2, "Server doesn't accept SSL connections at port 465")

        if self.results[1]:
            self.logger.log(1, "Server supports STARTTLS")
        else:
            self.logger.log(3, "Server doesn't support STARTTLS")

tester = SslTester