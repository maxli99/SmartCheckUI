# -*- coding: utf-8 -*-

import json

from flask import Blueprint, abort, request
from jinja2 import TemplateNotFound

from Exscript import Account

from web.widget.render import render

setting = Blueprint('setting', __name__,
                    template_folder='templates')

jsmodules = []
styles = []

@setting.route('/', methods = ['GET'])
def index():
    try:
        return render('unofficial/commingsoon.html')
    except TemplateNotFound:
        abort(404)
