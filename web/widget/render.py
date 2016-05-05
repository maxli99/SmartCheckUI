# -*- coding: utf-8 -*-

import os
import sys
from flask import render_template, request

from web.widget.nav import get_nav
from web.model.setting import is_initiated

def render(template_name, **arg):
    return render_template(template_name, request=request, reloading=False, nav=get_nav(), config_blink=(not is_initiated()),**arg).encode("utf-8")
