#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bootstrap import initialize
initialize()

from flask import abort, send_from_directory, redirect, url_for
from jinja2 import TemplateNotFound

from utils.sc_globals import sc_globals
from web.widget.render import render
from web.model.setting import is_initiated

app = sc_globals.APP

#blueprint
from web.test import test
from web.ne import ne
from web.setting import setting
from web.collector import collector
app.register_blueprint(test, url_prefix="/test")
app.register_blueprint(ne, url_prefix="/ne")
app.register_blueprint(setting, url_prefix="/setting")
app.register_blueprint(collector, url_prefix="/collector")

@app.route('/')
def index():
    if not is_initiated():
        return redirect(url_for("setting.index"))
    try:
        return render('index.html')
    except TemplateNotFound:
        abort(404)

@app.route('/img/<filename>')
def img_resource_redirect(filename):
    return send_from_directory('static/img', filename)

if __name__ == '__main__':
    app.run("0.0.0.0", port=sc_globals.SERVICE_PORT)
