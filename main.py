#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
from time import sleep
import requests
from websocket import create_connection
from base64 import b64decode
import json


FILEDIR = os.path.dirname(os.path.abspath(__file__))
MDHTML = 'mdToHtml.py'
SLEEPTIME = 10


def main():
    """"""
    subprocess.run([os.path.join(FILEDIR, MDHTML), sys.argv[1]])
    fname, _ = os.path.splitext(sys.argv[1])
    nameHTML = fname + '.html'
    namePDF = fname + '.pdf'
    server = subprocess.Popen(['python3', '-m', 'http.server'])
    headlesschr = subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--headless', '--remote-debugging-port=9222', '--disable-gpu', 'http://localhost:8000/'+nameHTML])
    sleep(SLEEPTIME)
    res = requests.get('http://localhost:9222/json')
    args = {
        "method": "Page.printToPDF",
        "id": 1}
    ws = create_connection(res.json()[0]['webSocketDebuggerUrl'])
    ws.send(json.dumps(args))
    rs = ws.recv()
    ws.close()
    server.terminate()
    headlesschr.terminate()
    data = json.loads(rs)
    f = open(os.path.join(FILEDIR, namePDF), 'wb')
    f.write(b64decode(data.get('result', {}).get('data', '')))
    f.close()


if __name__ == '__main__':
    main()
