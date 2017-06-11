#!/usr/bin/env python
import os

#see twilio API for how to text yourself via the command line using cURL
def textReminder(reminder):
    command = "curl -X POST 'https://api.twilio.com/2010-04-01/Accounts/[redacted]/Messages.json'         --data-urlencode 'To=[mynumber]'         --data-urlencode 'From=[mytwilionumber]'         --data-urlencode 'DateSent=\"Wed, 7 Dec 2016 10:46:00 +0800\"'         --data-urlencode 'Body=\"" + reminder +"\"'         -u [redacted]"
    os.system(command)

