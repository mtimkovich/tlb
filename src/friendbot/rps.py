#!/usr/bin/env python3
import random
import sqlite3
import sys

conn = sqlite3.connect('rps.db')
c = conn.cursor()

class Player:
    rps = {
        0: 'rock',
        1: 'paper',
        2: 'scissors',
    }

    def __init__(self, name):
        self.name = name
        self.score = 0

    def play(self):
        return random.randint(0, 2)

    def win(self):
        c.execute('update rps set score = score + 1 where name = ?', (self.name,))
        c.execute('select score from rps where name = ?', (self.name,))
        self.score = c.fetchone()[0]

    @classmethod
    def vs(cls, one, two):
        output = ''

        a = one.play()
        b = two.play()

        output += '{} played {}\n'.format(one.name, cls.rps[a])
        output += '{} played {}\n'.format(two.name, cls.rps[b])

        if a == b:
            output += 'TIE!'
        elif a == (b + 1) % 3:
            one.win()
            output += '{} wins! Score: {}'.format(one.name, one.score)
        else:
            two.win()
            output += '{} wins! Score: {}'.format(two.name, two.score)

        return output

# text = 'max vs jonat'
text = 'leaderboard'
text = text.lower()
args = text.split()

if args[0] == 'leaderboard':
    c.execute('select name, score from rps order by score desc, name')
    output = ''

    for i, row in enumerate(c.fetchmany(10)):
        output += '{}. {} ({})\n'.format(i+1, row[0], row[1])

    print(output)

    sys.exit()
elif len(args) != 3 or args[1].replace('.', '') not in ('vs', 'versus'):
    print("Usage:", "[one] vs [two]")
    sys.exit()

one = Player(args[0])
two = Player(args[2])

output = Player.vs(one, two)
print(output)

conn.commit()
conn.close()
