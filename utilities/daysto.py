#!/usr/bin/env python3 -tt

"""Usage:
  daysto.py DATE

Options:
  -h --help           show this HELP message and exit
"""

#print('Usage: daysto 01-01-2100')
import datetime
import json
import maya
import re
import sys
from docopt import docopt

def james_date_to_epoch(james_date):
    parts = james_date.split('-')
    if len(parts) != 4:
        raise ValueError("Bad Time Syntax!")
    month = parts[0]
    day = parts[1]
    year = parts[2]
    maya_format = '{}-{}-{} {}:{}'.format(year, month, day, 0, 0)
    return maya.when(maya_format,timezone=timezone)

def get_midnight(timezone):
    now = maya.now()
    local_now = now.datetime(to_timezone=timezone, naive=True)
    year = local_now.year
    month = local_now.month
    day = local_now.day
    midnight = maya.when('-'.join(map(str,[year, month, day])), timezone=timezone)
    return midnight

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Reminders 0.1')
    with open('/Users/jamesshapiro/scripts/lambda_creds', 'r') as json_data:
        d = json.load(json_data)
    timezone = d['timezone']
    target_day = arguments['DATE']
    midnight = get_midnight(timezone)
    target_midnight = james_date_to_epoch(target_day + '-12am')
#    print(midnight, target_midnight)
    total = 0
    while midnight._epoch < target_midnight._epoch:
        midnight = midnight.add(days=1)
        total += 1
    print(total)
#    while midnight.epoch > target_midnight._epoch:

