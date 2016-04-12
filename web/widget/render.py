# -*- coding: utf-8 -*-

import os
import sys
from flask import render_template

def render(template_name, **arg):
    return render_template(template_name, reloading=False, **arg).encode("utf-8")
