#!/usr/bin/env python3
import csv
import datetime
from slackclient import SlackClient
import yaml

# Change channel to '#livingroom' in production
def post(sc, text):
    sc.api_call(
        'chat.postMessage',
        username='birthdaybot',
        icon_emoji=':cake:',
        channel='#test',
        text=text,
        parse='full'
    )

today = datetime.datetime.now().strftime('%-m-%-d')
birthdayers = []

with open('birthdays.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if today == row['birthday']:
            birthdayers.append(row)

with open('slack_token.yml') as f:
    slack_token = yaml.load(f)['token']

sc = SlackClient(slack_token)

for i, friend in enumerate(birthdayers):
    post(sc, 'HAPPY BIRTHDAY, {name}!!! @{user} :cake:'.format(**friend))

    if i < len(birthdayers) - 1:
        post(sc, 'AND')
