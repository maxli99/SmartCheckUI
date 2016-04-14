# -*- coding: utf-8 -*-

import json

from flask import Blueprint, abort, request, jsonify
from jinja2 import TemplateNotFound

from Exscript import Account

from web.widget.render import render

test = Blueprint('test', __name__,
                    template_folder='templates')

jsmodules = ['test']
styles = ['']

@test.route('/', methods = ['GET'])
def index():
    try:
        return render('unofficial/test.html', jsmodules=jsmodules)
    except TemplateNotFound:
        abort(404)

@test.route('/', methods = ['POST'])
def get_result():
    try:
        data = request.get_json(True)
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

        response = str(conn.response)

        from ansi2html import Ansi2HTMLConverter
        from html2text import HTML2Text
        conv = Ansi2HTMLConverter()
        h2t = HTML2Text()
        response = h2t.handle(conv.convert(response))

        conn.send('exit\n')
        conn.close()
        return jsonify(success=True, response=response)
    except Exception as e:
        return jsonify(success=False, response="Opus! Some guy poisoned my coffee last night!")
