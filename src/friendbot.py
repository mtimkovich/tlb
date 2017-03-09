#!/usr/bin/env python3
import cgi
import json
import os
import random
import sys

# Map users to names
# Jonat doesn't need to be on here lol
friend_map = {
    'justinatlaw': 'justin',
    'chandyland': 'claire',
    'zarol': 'jay',
    'childish-landrito': 'ernest',
    'bobo': 'boston',
    'djswerve': 'max'
}


def is_comment(s):
    return s.startswith('//')


def randline(filename):
    """
    Prefix a line with // to comment it
    """
    output = ''

    with open(filename) as f:
        for line in f:
            if not is_comment(line):
                output = line
                break

        i = 1
        for line in f:
            if is_comment(line):
                continue

            if not random.randint(0, i):
                output = line
            i += 1

    return output.rstrip()


def tag_in_trigger(msg, friend):
    """
    Check if trigger text has a tag as a substring
    """
    return bool([name for tag, name in friend_map.items()
                if tag in trigger and name == friend])

if os.environ['REQUEST_METHOD'] != 'POST':
    print(
"""Status: 403 Forbidden
Content-Type: text/html

<h1>Forbidden</h1>
<p>You don't have permission to access /friendbot.py on this server.
""")
    sys.exit(1)

print('Content-Type: application/json\n')

form = cgi.FieldStorage()

trigger = form.getvalue('trigger_word', '')
domain = form.getvalue('team_domain', '')
user = form.getvalue('user_name', '${name}')

if domain != 'thelonelybear':
    sys.exit(1)

for txt in os.listdir('friends'):
    file_name = os.path.splitext(txt)[0]

    if file_name in trigger or tag_in_trigger(trigger, file_name):
        output = randline(os.path.join('friends', txt))

        # var replacement
        output = output.replace('${name}', user)
        output = output.replace('${newline}', '\n')

        print(json.dumps({'text': output}))
        break
