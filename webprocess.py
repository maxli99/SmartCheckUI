#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bootstrap import initialize
initialize()

from flask import Flask, redirect, url_for, abort, send_from_directory
from jinja2 import TemplateNotFound

from utils.sc_globals import sc_globals
from web.widget.render import render

app = Flask(sc_globals.APP_NAME)
app.config['SECRET_KEY'] = 'scui'
app.config['UPLOAD_FOLDER'] = 'tmp'
app.config['MAX_CONTENT_LENGTH'] = 16777216

app.debug = sc_globals.DEBUG
app.use_reloader = False

#session
app.secret_key = '\x80p;\x05\\}\xba\x8bd\xd8\xb0M#`B\xe9\x8c\x07"\xb0Q&V\xb5"`'

#blueprint
from web.test import test
from web.config import config
from web.setting import setting
app.register_blueprint(test, url_prefix="/test")
app.register_blueprint(config, url_prefix="/config")
app.register_blueprint(setting, url_prefix="/setting")

@app.route('/')
def index():
    try:
        return render('index.html')
    except TemplateNotFound:
        abort(404)

@app.route('/img/<filename>')
def img_resource_redirect(filename):
    return send_from_directory('static/img', filename)

if __name__ == '__main__':
    app.run("0.0.0.0", port=sc_globals.SERVICE_PORT)
