#!/usr/bin/env python3
import os
import pytest
import requests
import shutil
import subprocess as sp
import time

URL = 'http://localhost:3000/cgi-bin/friendbot.py'


def get_trigger(text):
    return {
        'team_domain': 'thelonelybear',
        'trigger_word': text,
        'text': text
    }


def in_corpus(text, friend):
    with open('cgi-bin/friends/{}.txt'.format(friend)) as f:
        for line in f:
            if text == line.rstrip():
                return True
        else:
            return False


@pytest.fixture(scope='module')
def server():
    """
    Copy program files to cgi-bin
    Modify source so it works with this impromptu server
    """

    files = ['friends', 'friendbot.py']

    for fh in files:
        src = '../src/' + fh
        dst = 'cgi-bin/' + fh
        copy = shutil.copy if os.path.isfile(src) else shutil.copytree
        copy(src, dst)

    # Replace the friends_dir value
    sp.call(['perl', '-i', '-pe', "s#friends_dir = .*#friends_dir = 'cgi-bin/friends'#", 'cgi-bin/friendbot.py'])
    p = sp.Popen('python3 -m http.server --cgi 3000'.split())
    time.sleep(1)

    yield

    """
    Stop server process
    rm -rf cgi-bin/*
    """

    for fh in files:
        src = '../src/' + fh
        dst = 'cgi-bin/' + fh
        remove = os.remove if os.path.isfile(src) else shutil.rmtree
        remove(dst)

    p.terminate()


def test_server(server):
    """
    Make sure the server started up correctly
    """
    r = requests.get('http://localhost:3000')
    assert r.status_code == 200


def test_exclamation(server):
    friend = 'justin'
    params = get_trigger('!{}bot'.format(friend))
    r = requests.post(URL, data=params)

    assert r.text, 'Empty response'

    text = r.json()['text']
    valid = in_corpus(text, friend)
    assert valid, 'Invalid response'


def test_mention(server):
    friend = 'justin'
    params = get_trigger('<@U406YM1JL')
    r = requests.post(URL, data=params)

    assert r.text, 'Empty response'

    text = r.json()['text']
    valid = in_corpus(text, friend)
    assert valid, 'Invalid response'


def test_file_upload(server):
    params = get_trigger('<@U406YM1JL')
    params['text'] += ' uploaded a file'
    r = requests.post(URL, data=params)

    assert not r.text, 'Response should be empty'
