#!/usr/bin/env python3
import cgi
import json
import os
import random
import sys


def randline(filename):
    """
    Prefix a line with # to comment it
    """
    output = ''

    with open(filename) as f:
        for line in f:
            if not line.startswith('#'):
                output = line
                break

        i = 1
        for line in f:
            if line.startswith('#'):
                continue

            if not random.randint(0, i):
                output = line
            i += 1

    return output.rstrip()

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

text = form.getvalue('trigger_word', '')
domain = form.getvalue('team_domain', '')
user = form.getvalue('user_name', '${name}')

if domain != 'thelonelybear':
    sys.exit(1)

if not text.startswith('!') and not text.endswith('bot'):
    sys.exit(1)

friend = text[1:-3]

for txt in os.listdir('friends'):
    file_name = os.path.splitext(txt)[0]

    if friend == file_name:
        output = randline(os.path.join('friends', txt))

        # var replacement
        output = output.replace('${name}', user)
        output = output.replace('${newline}', '\n')

        print(json.dumps({'text': output}))
        break
