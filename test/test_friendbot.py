#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler
import os
import pytest
import requests
from socketserver import TCPServer
import threading
import time

URL = 'http://localhost:3000/cgi-bin/friendbot.py'

def get_trigger(text):
    return {
        'team_domain': 'thelonelybear',
        'trigger_word': text,
        'text': text
    }

def get_server():
    server_address = ('', 3000)
    TCPServer.allow_reuse_address = True
    httpd = TCPServer(server_address, SimpleHTTPRequestHandler)

    return httpd

@pytest.fixture(scope='module')
def server():
    """
    Copy program files to cgi-bin
    Modify source so it works with this impromptu server
    """

    # sp.call(['perl', '-i', '-pe', "s#friend_dir = .*#friend_dir = 'cgi-bin/friends'#", 'cgi-bin/friendbot.py'])
    # p = sp.Popen('python3 -m http.server --cgi 3000'.split())
    server = get_server()
    threading.Thread(target=server.serve_forever).start()
    time.sleep(1)

    yield


    """
    Stop server process
    rm -rf cgi-bin/*
    """

    server.shutdown()
    server.server_close()

def test_server(server):
    r = requests.get('http://localhost:3000')
    assert r.status_code == 200

# def test_exclamation(server):
#     params = get_trigger('!justinbot')
#     r = requests.post(URL, data=params)
#     assert r.text, 'Empty response from server'

