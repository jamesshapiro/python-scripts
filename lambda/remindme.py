#!/usr/bin/env python3 -tt

import requests
import json
import sys
import maya

if len(sys.argv) != 2:
    print('Usage: remindme "do laundry" 12-18-2016-12:09:53:am')
    sys.exit(0)

with open('/Users/jamesshapiro/scripts/lambda_password', 'r') as f:
    password = f.read().replace('\n', '')

with open('/Users/jamesshapiro/scripts/lambda_link', 'r') as f:
    url = f.read().replace('\n', '')

reminder = sys.argv[1]
now = maya.now()
later = now.add(minutes=0)
later_int = int(later._epoch)

payload = {'reminder': reminder,
           'password': password,
           'time': str(later_int)}

r = requests.post(url, data=json.dumps(payload))

print(r.text)
to_json = json.loads(r.text)
print(to_json['message'])
