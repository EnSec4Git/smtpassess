__author__ = 'Yavor-Nb'
import imaplib

#TODO: Add support for POP3

class MailAccess:
    def __init__(self, configuration):
        self._protocol = configuration.get("access", "proto")
        if self._protocol not in ["IMAP"]:
             raise ValueError("Access protocol is unknown or not supported")
        self._username = configuration.get("access", "username")
        self._host = configuration.get("access", "host")
        self._password = configuration.get("access", "password")
        #self._connection = imaplib.IMAP4(self._host)

    def search(self, frm, to, text):
        criteria = []
        if frm:
            criteria.append('FROM')
            criteria.append("'" + frm + "'")
        if to:
            criteria.append('TO')
            criteria.append("'" + to + "'")
        if text:
            criteria.append('BODY')
            criteria.append("'" + text + "'")
        #return self._connection.search(*criteria)