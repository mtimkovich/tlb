#!/usr/bin/env python3
import cgi
import json
import os
import random
import sys


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

# Map Slack IDs to names
friend_map = {
    'U406YM1JL': 'justinatlaw',
    'U40UP9YEN', 'chandyland',
    'U407FJ7KK', 'zarol',
    'U407EU12M', 'childish-landrito',
    'U407JD1K3', 'bobo',
    'U410D66MA': 'djswerve',
    'U40SH115Z': 'jonat'
}

if text.startswith('!') and text.endswith('bot'):
    friend = text[1:-3]
elif text.startswith('<@'):
    friend = friend_map[text[2:]]
else:
    sys.exit(1)

for txt in os.listdir('friends'):
    file_name = os.path.splitext(txt)[0]

    if friend == file_name:
        output = randline(os.path.join('friends', txt))

        # var replacement
        output = output.replace('${name}', user)
        output = output.replace('${newline}', '\n')

        print(json.dumps({'text': output}))
        break
