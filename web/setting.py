# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, abort, request, redirect, url_for, flash

from web.widget.render import render
from model.setting import Dao

setting = Blueprint('setting', __name__,
                    template_folder='templates')

jsmodules = ['setting']
styles = []

@setting.route('/', methods=['GET', 'POST'])
def index():
    dao = Dao()
    if request.method == "GET":
        try:
            project = ""
            email = ""
            settings = dao.getall()
            for setting in settings:
                if setting.key == 'project':
                    project = setting.value
                if setting.key == 'email':
                    email = setting.value
        except Exception as e:
            logging.error(e)
        return render('page/setting.html', project=project, email=email, jsmodules=jsmodules)

    elif request.method == "POST":
        try:
            settings = dao.getall()
            project = (request.form['project'])
            email = (request.form['email'])
            for setting in settings:
                if setting.key == 'project':
                    setting.value = project
                if setting.key == 'email':
                    setting.value = email
            dao.update()
            flash(True)
        except Exception as e:
            logging.error(e)
            flash(False)
        return redirect(url_for(".index"))
    else:
        abort(404)
