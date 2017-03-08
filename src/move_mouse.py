#!/usr/bin/python
"""
This is for keeping Ernest's computer awake while playing Smash

Requires autopy from https://github.com/msanders/autopy
"""
import autopy
import time


def move(x, y):
    try:
        autopy.mouse.move(x, y)
        time.sleep(1)
    except ValueError:
        pass

while True:
    x, y = autopy.mouse.get_pos()

    move(x+5, y+5)
    move(x+5, y-5)
    move(x-5, y-5)
    move(x-5, y+5)
    move(x, y)

    time.sleep(60)
