#!/usr/bin/env python3 -tt

"""Usage:
  remindme.py REMINDER TIME ... [options]

Options:
  -h --help           show this HELP message and exit
  --repeat FREQUENCY  repeat reminder with frequency
  --until STOP        repeat until, e.g. 5-14-2020-9:15am [default: '1-1-2038-12:00am']
"""

#now.datetime(to_timezone='US/Pacific', naive=True)
#print('Usage: remindme "do laundry" 12-18-2016-12:09:am')

import json
import maya
import re
import requests
import sys
from docopt import docopt

"""
today, tomorrow, M-Sun, next week, tonight
"""

def time_of_day(time):
    # 8am, 8pm, 12am, 8:30am, 8:30pm, 12:30pm
    pattern = re.compile('(\d\d?)(:(\d\d))?(am|pm)')
    if pattern.match(time):
        hour = int(pattern.match(time).groups()[0])
        ampm = pattern.match(time).groups()[3]
        minute = pattern.match(time).groups()[2]
        if minute == None:
            minute = 0
        minute = int(minute)
    else:
        print('INVALID TIME FORMAT')
        print('try: 8am, 8:30am, 12pm, 12:17pm')
        sys.exit(0)
    if hour == 12:
        hour = 0
    if ampm == 'pm':
        hour += 12
    return (hour, minute)

def james_date_to_epoch(james_date):
    parts = james_date.split('-')
    if len(parts) != 4:
        raise ValueError(bad_time_syntax)
    month = parts[0]
    day = parts[1]
    year = parts[2]
    hour, minute = time_of_day(parts[3])
    maya_format = '{}-{}-{} {}:{}'.format(year, month, day, hour, minute)
    return maya.when(maya_format,timezone=timezone)

def get_midnight(timezone):
    now = maya.now()
    local_now = now.datetime(to_timezone=timezone, naive=True)
    year = local_now.year
    month = local_now.month
    day = local_now.day
    midnight = maya.when('-'.join(map(str,[year, month, day])), timezone=timezone)
    return midnight

def upload_reminder(time, reminder, password, url):
    payload = {'reminder': reminder,
               'password': password,
               'time': time}
    r = requests.post(url, data=json.dumps(payload))
    to_json = json.loads(r.text)
    print(to_json['message'])

#TODO: add Sunday, Mon-Fri, Sat, next week, next month    
def parse_time(time, midnight):
    if time[0].endswith('am') or time[0].endswith('pm'):
        return james_date_to_epoch(time[0])
    if time[-1].endswith('am') or time[-1].endswith('pm'):
        hours, minutes = time_of_day(time[-1])
    if time == ['tonight']:
        return midnight.add(hours=20)
    if time == ['tomorrow', 'morning']:
        return midnight.add(days=1, hours=8)
    if time[0] == 'today':
        return midnight.add(hours=hours, minutes=minutes)
    if time[0] == 'tomorrow':
        return midnight.add(days=1, hours=hours, minutes=minutes)
    return midnight

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Reminders 0.1')
    print(arguments)
    with open('/Users/jamesshapiro/scripts/lambda_creds', 'r') as json_data:
        d = json.load(json_data)
    password = d['password']
    url = d['url']
    timezone = d['timezone']
    reminder = arguments['REMINDER']
    midnight = get_midnight(timezone)
    time = parse_time(arguments['TIME'], midnight)
    time = str(int(time._epoch))
    #TODO: finish implementing repeating reminders
    upload_reminder(time, reminder, password, url)
    if arguments['--repeat']:
        stop_date = james_date_to_epoch(arguments['--until'])
        print(int(stop_date._epoch))

"""
now = maya.now()
later = now.add(minutes=0)
later_int = int(later._epoch)
"""

#when = maya.when('2018-02-01', timezone='US/Pacific')