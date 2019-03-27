import json
import sys
import dateutil.parser
import time
import boto3
import os
from base64 import b64decode

bad_time_syntax = 'Bad time syntax. Usage: "reminder": "do laundry", "time": "12-18-2016-12:09am"'

ENCRYPTED = os.environ['ciphertext_password']
password = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED))['Plaintext'].decode("utf-8")

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
    readable_reminder_time = body['readable_reminder_time']
    
    message = "Remind James of the following: \"" + reminder_content + "\" at " + readable_reminder_time
    message += ". timestamp = {}".format(time_content)
    
    unixTime = int(body['time'])
    
    currUnixTime = int(str(time.time()).split(".")[0])
    message += ". lambda unix time = {}".format(currUnixTime)
    if currUnixTime > unixTime:
        message += " ***WARNING: REMINDER IS IN THE PAST!***"
        message += " {} < {}".format(unixTime, currUnixTime)
    
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
