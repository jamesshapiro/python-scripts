#!/usr/bin/env python3 -tt

import os
import sys

if len(sys.argv) != 3:
    print('Usage: remindme "do laundry" 12-18-2016-12:09:53:am')
    sys.exit(0)

thingToRemember = sys.argv[1]
jamesDate = sys.argv[2]
password = '[REDACTED]'

command = "curl -v -X POST "
command += "  'https://[REDACTED].execute-api.us-east-1.amazonaws.com/test/S' "
command += "  -H 'content-type: application/json' "
command += "  -H 'day: Friday' "
command += "  -H 'x-amz-docs-region: us-west-2' "
command += "  -d '{\"reminder\":\"" + thingToRemember + "\", "
command += "\"password\": \"" + password + "\","
command += "\"time\": \"" + jamesDate + "\"}'"

os.system(command)
