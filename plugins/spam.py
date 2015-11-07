__author__ = 'Yavor-Nb'

import smtplib
import time
from email.mime.text import MIMEText
import tools
import socket

NONEXISTENT_DOMAIN = "vbnmmnbvcbnmkjhvcx.com"
NONEXISTENT_SUBDOMAIN = "vbnmmnbvcbnmkjhvcx.register.bg"
DOMAIN_WITHOUT_SPF = "ctfbg.org"
EICAR_VALUE = "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
own_domain = socket.getfqdn()

class SpamTester:
    def __init__(self, logger, configuration):
        self.logger = logger
        self.strings = []
        self.timeout = 5
        if configuration.has_option("general", "test_timeout"):
            self.timeout = configuration.get("general", "test_timeout")
        self.target_email = configuration.get("target", "target_email")

    def perform_tests(self, target):
        # Test 1: Check if server accepts mail from invalid domain
        smtpobj = smtplib.SMTP(target[0], target[1])
        smtpobj.helo()

        unique_str = tools.random_string(20)
        self.strings.append(unique_str)
        invalid_sender = "admin@" + NONEXISTENT_DOMAIN
        msg = MIMEText(unique_str)
        msg['Subject'] = 'Test'
        msg['From'] = invalid_sender
        msg['To'] = self.target_email
        try:
            smtpobj.sendmail(invalid_sender, self.target_email, msg)
            smtpobj.quit()
        except:
            pass

        time.sleep(self.timeout)

        # Test 2: Check if server accepts mail from invalid subdomain
        smtpobj = smtplib.SMTP(target[0], target[1])
        smtpobj.helo()

        unique_str = tools.random_string(20)
        self.strings.append(unique_str)
        invalid_sender = "admin@" + NONEXISTENT_SUBDOMAIN
        msg = MIMEText(unique_str)
        msg['Subject'] = 'Test'
        msg['From'] = invalid_sender
        msg['To'] = self.target_email
        try:
            smtpobj.sendmail(invalid_sender, self.target_email, msg)
            smtpobj.quit()
        except:
            pass

        time.sleep(self.timeout)

        # Test 3: Check if server will accept email from a domain without SPF
        smtpobj = smtplib.SMTP(target[0], target[1])
        smtpobj.helo()

        unique_str = tools.random_string(20)
        self.strings.append(unique_str)
        invalid_sender = "admin@" + DOMAIN_WITHOUT_SPF
        msg = MIMEText(unique_str)
        msg['Subject'] = 'Test'
        msg['From'] = invalid_sender
        msg['To'] = self.target_email
        try:
            smtpobj.sendmail(invalid_sender, self.target_email, msg)
            smtpobj.quit()
        except:
            pass

        time.sleep(self.timeout)

        # Test 4: Check if server will accept email with different MAIL FROM and From: header
        smtpobj = smtplib.SMTP(target[0], target[1])
        smtpobj.helo()

        unique_str = tools.random_string(20)
        self.strings.append(unique_str)
        invalid_sender = "admin@" + own_domain
        msg = MIMEText(unique_str)
        msg['Subject'] = 'Test'
        msg['From'] = "admin@google.com"
        msg['To'] = self.target_email
        try:
            smtpobj.sendmail(invalid_sender, self.target_email, msg)
            smtpobj.quit()
        except:
            pass

        time.sleep(self.timeout)

    def check_results(self, mail_access):
        if mail_access.search(None, None, self.strings[0]):
            self.logger.log(2, "Server accepts mails from an invalid domain")
        else:
            self.logger.log(1, "Server rejected mails from an invalid domain")

        if mail_access.search(None, None, self.strings[1]):
            self.logger.log(2, "Server accepts mails from an invalid subdomain")
        else:
            self.logger.log(1, "Server rejects mails from an invalid subdomain")

        if mail_access.search(None, None, self.strings[2]):
            self.logger.log(2, "Server accepts email from a domain without SPF")
        else:
            self.logger.log(1, "Server refuses email from a domain without SPF")

        if mail_access.search(None, None, self.strings[3]):
            self.logger.log(2, "Server accepts mail with different MAIL FROM and From:")
        else:
            self.logger.log(1, "Server accepts mail with different MAIL FROM and From:")

tester = SpamTester