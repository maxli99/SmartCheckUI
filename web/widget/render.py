# -*- coding: utf-8 -*-

import os
import sys
from flask import render_template

from web.utils.nav import get_nav

def render(template_name, **arg):
    return render_template(template_name, reloading=False, nav=get_nav(), **arg).encode("utf-8")
