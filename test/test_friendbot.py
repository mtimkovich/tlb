#!/usr/bin/env python3
import os
import pytest
import requests
import subprocess as sp
import time

URL = 'http://localhost:3000/cgi-bin/friendbot.py'

def get_trigger(text):
    return {
        'team_domain': 'thelonelybear',
        'trigger_word': text,
        'text': text
    }

@pytest.fixture(scope='module')
def server():
    """
    Create cgi-bin directory
    Copy program files to cgi-bin
    Modify source so it works with this impromptu server
    """

    sp.call(['perl', '-i', '-pe', "s#friend_dir = .*#friend_dir = 'cgi-bin/friends'#", 'cgi-bin/friendbot.py'])
    p = sp.Popen('python3 -m http.server --cgi 3000'.split())
    time.sleep(1)
    yield

    """
    Stop server process
    rm -rf cgi-bin
    """

    p.kill()

def test_exclamation(server):
    params = get_trigger('!justinbot')
    r = requests.post(URL, data=params)
    assert r.text, 'Empty response from server'
