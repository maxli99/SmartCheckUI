# -*- coding: utf-8 -*-

import json

from flask import Blueprint, abort, request
from jinja2 import TemplateNotFound

from Exscript import Account

from web.widget.render import render

config = Blueprint('config', __name__,
                    template_folder='templates')

jsmodules = []
styles = []

@config.route('/', methods = ['GET'])
def index():
    try:
        return render('unofficial/commingsoon.html', jsmodules=jsmodules)
    except TemplateNotFound:
        abort(404)
