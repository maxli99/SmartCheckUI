# -*- coding: utf-8 -*-

import json

from flask import Blueprint, abort, request
from jinja2 import TemplateNotFound

from Exscript import Account

from web.widget.render import render

test = Blueprint('test', __name__,
                    template_folder='templates')

jsmodules = ['test']

@test.route('/', methods = ['GET'])
def index():
    try:
        return render('test.html', jsmodules=jsmodules)
    except TemplateNotFound:
        abort(404)

@test.route('/', methods = ['POST'])
def get_result():
    try:
        data = json.loads(request.data.decode('utf-8'))
        address = data['host']
        account = Account(name=data['user'], password=data['passwd'])

        if data['conntype'] == 'SSH':
            from Exscript.protocols import SSH2
            conn = SSH2()
        elif data['conntype'] == 'Telnet':
            from Exscript.protocols import Telnet
            conn = Telnet()
        else:
            raise(Exception('Unsupport connection type'))
        conn.connect(address)
        conn.login(account)
        conn.execute(data['command'])
        response = repr(conn.response)
        conn.send('exit\n')
        conn.close()
        return response
    except Exception as e:
        print(e)
        return "Opus! Some guy poisoned my coffee last night! I'm 狗'in 带!!"
    return response
