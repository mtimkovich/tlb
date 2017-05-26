#!/usr/bin/env python3
import csv
import datetime
from slackclient import SlackClient
import yaml

with open('config.yml') as f:
    config = yaml.load(f)

sc = SlackClient(config['token'])

def post(text):
    sc.api_call(
        'chat.postMessage',
        username='birthdaybot',
        icon_emoji=':cake:',
        channel=config['channel'],
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

for i, friend in enumerate(birthdayers):
    post('HAPPY BIRTHDAY, {name}!!! @{user} :cake:'.format(**friend))

    if i < len(birthdayers) - 1:
        post('AND')
