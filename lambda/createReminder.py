import json
import sys
import dateutil.parser
import time
import boto3

bad_time_syntax = 'Bad time syntax. Usage: "reminder": "do laundry", "time": "12-18-2016-12:09:53:am"'
password = '[REDACTED]'

def badRequest(message):
    responseCode = 400
    responseBody = {'feedback': message}
    response = {'statusCode': responseCode,
                'headers': {'x-custom-header' : 'custom-header'},
                'body': json.dumps(responseBody)}
    return response

def unauthorizedRequest():
    responseCode = 401
    responseBody = {'feedback': 'bad password or missing password in body'}
    response = {'statusCode': responseCode,
                'headers': {'x-custom-header' : 'custom-header'},
                'body': json.dumps(responseBody)}
    return response

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

def lambda_handler(event, context):
    responseCode = 200
    print("request: " + json.dumps(event))
    
    if 'body' not in event:
        return badRequest('you have to include a request body')
    body = json.loads(event['body'])
    if 'password' not in body or body['password'] != password:
        return unauthorizedRequest()
    if 'reminder' not in body:
        return badRequest('the request body has to include a reminder')
    reminder_content = body['reminder']
    if 'time' not in body:
        return badRequest('the request body has to include a time')
    time_content = body['time']
    
    message = "Remind James of the following: \"" + reminder_content + "\" at " + time_content + ", Cali time. "
    message += ". time content = {}".format(time_content)
    try:
        iso8601Time = convertJamesDateToISO8601(time_content)
        message += '. iso8601Time = {}'.format(iso8601Time)
    except ValueError:
        return badRequest(bad_time_syntax)
    
    unixTime = convertISO8601ToUnixTimestamp(iso8601Time)
    
    currUnixTime = int(str(time.time()).split(".")[0])
    if currUnixTime > unixTime:
        message += "***WARNING: REMINDER IS IN THE PAST!***"
        message += "current time = {}. reminder time = {}".format(currUnixTime, unixTime)
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('reminders')
    while 'Item' in table.get_item(Key = {'unixtimestamp': unixTime}):
        unixTime += 1
    
    table.put_item(
        Item={
            'unixtimestamp': unixTime,
            'reminder': reminder_content
        }
    )
    responseBody = {
        'message': message,
        'input': event
    }
    
    response = {
        'statusCode': responseCode,
        'headers': {
            'x-custom-header' : 'custom header'
        },
        'body': json.dumps(responseBody)
    }
    print("response: " + json.dumps(response))
    return response

