#!/usr/bin/env python3 -tt

"""Usage:
  remindme.py REMINDER TIME ... [options]

Options:
  -h --help           show this HELP message and exit
  --repeat FREQUENCY  repeat reminder with frequency
  --until STOP        repeat until, e.g. 1-1-2020-9:00:00:am
"""

#now.datetime(to_timezone='US/Pacific', naive=True)
#print('Usage: remindme "do laundry" 12-18-2016-12:09:53:am')

import requests
import json
import sys
import maya
from docopt import docopt

"""
today, tomorrow, M-Sun, next week, tonight

"""
def get_midnight(timezone):
    print(timezone)
    now = maya.now()
    local_now = now.datetime(to_timezone=timezone, naive=True)
    year = local_now.year
    month = local_now.month
    day = local_now.day
    midnight = maya.when('-'.join(map(str,[year, month, day])), timezone=timezone)
    return int(midnight._epoch)

def upload_reminder(time, reminder, password, url):
    payload = {'reminder': reminder,
               'password': password,
               'time': str(time)}
    print(url, type(url))
    print(time, type(time))
    print(reminder, type(reminder))
    print(password, type(password))
    r = requests.post(url, data=json.dumps(payload))
    print(r.text)
    to_json = json.loads(r.text)
#    print(to_json['message'])

def parse_time(time, midnight):
    if time[0] == 'today':
        print('hooray!')

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Reminders 0.1')
    print(arguments)
    with open('/Users/jamesshapiro/scripts/lambda_creds', 'r') as json_data:
        d = json.load(json_data)
    password = d['password']
    url = d['url']
    timezone = d['timezone']
    reminder = arguments['REMINDER']
    midnight_timestamp = get_midnight(timezone)
    midnight = maya.when(str(midnight_timestamp), timezone=timezone)
    #time = parse_time(arguments['TIME'])
    time = midnight.add(hours=21,minutes=55)
    time = int(time._epoch)
    #    print(get_midnight(timezone))
    #    sys.exit(0)
    upload_reminder(time, reminder, password, url)

"""
now = maya.now()
later = now.add(minutes=0)
later_int = int(later._epoch)
"""

#when = maya.when('2018-02-01', timezone='US/Pacific')

def convertJamesDateToISO8601(dato):
    parts = dato.split("-")
    if len(parts) != 4:
        raise ValueError(bad_time_syntax)
    month = parts[0]
    day = parts[1]
    year = parts[2]
    time = parts[3]
    timeParts = time.split(":")
    if len(timeParts) != 4:
        raise ValueError(bad_time_syntax)
    hour = int(timeParts[0])
    minute = int(timeParts[1])
    second = int(timeParts[2])
    if hour < 1 or hour > 12 or minute < 0 or minute > 59 or second < 0 or second > 59:
        raise ValueError(bad_time_syntax)
    amOrPm = timeParts[3]
    if amOrPm != 'am' and amOrPm != 'pm':
        raise ValueError(bad_time_syntax)
    if hour == 12 and amOrPm == "am":
        hour = 0
    elif hour == 12 and amOrPm == "pm":
        hour = 12
    elif amOrPm == "pm":
        hour = hour + 12
    return year + "-" + month + "-" + day + "T" + str(hour) + ":" + str(minute) + ":" + str(second) + "-00:00"

def convertISO8601ToUnixTimestamp(iso8601):
    parsedDate = dateutil.parser.parse(iso8601)
    return int(time.mktime(parsedDate.timetuple())) + (8 * 3600)
