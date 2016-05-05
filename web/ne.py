# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, abort, request, jsonify, redirect, url_for, flash

from web.widget.render import render
from model.ne import Dao, NE

ne = Blueprint('ne', __name__,
                    template_folder='templates')

jsmodules = ['ne']
styles = []

@ne.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render('page/ne.html', jsmodules=jsmodules)
    if request.method == "POST":
        current = 0
        rowcount = 0
        search = ''
        sortkey = ''
        sorttype = ''
        for item in request.form:
            if item == 'current':
                current = int(request.form[item])
            if item == 'rowCount':
                rowcount = int(request.form[item])
            if item == 'searchPhrase':
                search = request.form[item]
            if item[0:5] == 'sort[':
                sortkey = item[5:-1]
                sorttype =request.form[item]
        dao = Dao()
        total = dao.get_total()
        nes = dao.get_page(current, rowcount, search, sorttype, sortkey)
        result = {"current": current,
                  "rowCount": rowcount,
                  "rows": [],
                  "total": total
                  }
        for ne in nes:
            result["rows"].append({"id": ne.id, "name": ne.name, "type": ne.type, "conntype": ne.conntype, "address": ne.address, "port": ne.port, "user": ne.user})
        return jsonify(result)

    else:
        abort(404)

@ne.route('/add', methods=['POST'])
def add():
    from pprint import pprint
    if request.method == "POST":
        try:
            name = request.form['name']
            address = request.form['host']
            user = request.form['user']
            password = request.form['passwd']
            type = request.form['type']
            conntype = request.form['conntype']
            port = int(request.form['port'])
            dao = Dao()
            dao.add(NE(name=name, type=type, conntype=conntype, address=address, port=port, user=user, password=password))
            flash(True)
        except Exception as e:
            logging.error(e)
            flash(False)
        return redirect(url_for(".index"))
    else:
        abort(404)

@ne.route('/edit', methods=['POST'])
def edit():
    from pprint import pprint
    if request.method == "POST":
        try:
            dao = Dao()
            id = request.form['id']
            ne = dao.get(id)

            ne.name = request.form['name']
            ne.address = request.form['host']
            ne.user = request.form['user']
            ne.password = request.form['passwd']
            ne.type = request.form['type']
            ne.conntype = request.form['conntype']
            ne.port = int(request.form['port'])
            dao.update()
            flash(True)
        except Exception as e:
            logging.error(e)
            flash(False)
        return redirect(url_for(".index"))
    else:
        abort(404)

@ne.route('/get', methods=['POST'])
def get():
    if request.method == "POST":
        data = request.get_json(True)
        id = data['id']
        dao = Dao()
        ne = dao.get(id)
        result = {"id": ne.id, "name": ne.name, "type": ne.type, "conntype": ne.conntype, "address": ne.address, "port": ne.port, "user": ne.user, "passwd": ne.password}
        return jsonify(ne=result)

@ne.route('/delete', methods=['POST'])
def delete():
    if request.method == "POST":
        try:
            data = request.get_json(True)
            id = data['id']
            dao = Dao()
            dao.remove(dao.get(id))
            return jsonify(success=True)
        except Exception as e:
            logging.error(e)
            return jsonify(success=False)

@ne.route('/verify', methods=['GET', 'POST'])
def verify():
    from Exscript import Account
    from web.widget.connector import MMETelnet, MMESSH2, SaegwTelnet, SaegwSSH2
    try:
        data = request.get_json(True)
        address = data['host']
        account = Account(name=data['user'], password=data['passwd'])
        port = int(data['port'])
        type = data['type']
        conntype = data['conntype']
        conn = None
        if type == "MME":
            if conntype == "Telnet":
                conn = MMETelnet()
            elif conntype == "SSH":
                conn = MMESSH2(verify_fingerprint=False)
        elif type == "SAEGW":
            if conntype == "Telnet":
                conn = SaegwTelnet()
            elif conntype == "SSH":
                conn = SaegwSSH2(verify_fingerprint=False)
        if conn == None:
            raise Exception("Unsupported NE type [%s] or connection type [%s]."%(type, conntype))

        conn.connect(address, port)
        conn.login(account)
        conn.logout()
        conn.close()
        return jsonify(success=True)
    except Exception as e:
        logging.error(e)
        return jsonify(success=False)
