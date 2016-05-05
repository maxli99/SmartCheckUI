# -*- coding: utf-8 -*-
import logging
import os
import time
import zipfile
import base64

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from flask import Blueprint, request, jsonify, send_from_directory

from web.widget.render import render
from web.widget.worker import WorkerManager

from web.model.collector import get_modules, get_module, get_all_modules
from web.model.ne import Dao
from web.model.setting import Dao as SettingDao

from utils.sc_globals import sc_globals

collector = Blueprint('collector', __name__,
                    template_folder='templates')

jsmodules = ['collector']
styles = []

@collector.route('/', methods=['GET', 'POST'])
def index():
    return render('page/collector.html', jsmodules=jsmodules)


@collector.route('/getitems', methods=['GET', 'POST'])
def getitems():
    current = 0
    rowcount = 0
    search = ''
    for item in request.form:
        if item == 'current':
            current = int(request.form[item])
        if item == 'rowCount':
            rowcount = int(request.form[item])
        if item == 'searchPhrase':
            search = request.form[item]

    modules, total = get_modules(current, rowcount, search)
    result = {"current": current,
              "rowCount": rowcount,
              "rows": [],
              "total": total
              }
    for module in modules:
        result["rows"].append({"id":module.id, "name": module.name, "type": module.type})
    return jsonify(result)

@collector.route('/getitem', methods=['GET', 'POST'])
def getitem():
    if request.method == "POST":
        data = request.get_json(True)
        id = data['id']
        module = get_module(id)
        if module is not None:
            result = {"id": module.id, "name": module.name, "type": module.type, \
                      "cond": module.cond, "desc": module.desc, "oper": module.oper}
            return jsonify(success=True, module=result)
        else:
            return jsonify(success=False)

@collector.route('/getne', methods=['GET', 'POST'])
def getne():
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
            result["rows"].append({"id": ne.id, "name": ne.name, "type": ne.type, "address": ne.address})
        return jsonify(result)

@collector.route('/precheck', methods=['GET', 'POST'])
def precheck():
    data = request.get_json(True)
    nes = data['ne']
    items = data['item']
    response = {
        "ne_mme" : [],
        "item_mme" : [],
        "ne_saegw" : [],
        "item_saegw" : [],
        "ne_mme_desc" : "",
        "item_mme_desc" : "",
        "ne_saegw_desc" : "",
        "item_saegw_desc" : ""
    }
    dao = Dao()
    for ne in nes:
        if not nes[ne]:
            continue
        ne_detail = dao.get(int(ne))
        if ne_detail.type == "MME":
            response["ne_mme"].append(ne)
            response["ne_mme_desc"] += "%s\r\n"%ne_detail.name
        if ne_detail.type == "SAEGW":
            response["ne_saegw"].append(ne)
            response["ne_saegw_desc"] += "%s\r\n"%ne_detail.name

    for item in items:
        if not items[item]:
            continue
        item_detail = get_module(str(item))
        if item_detail.type == "flexins" and hasattr(item_detail.module, "get_log"):
            response["item_mme"].append(item)
            response["item_mme_desc"] += "%s\r\n"%item_detail.name
        if item_detail.type == "flexing" and hasattr(item_detail.module, "get_log"):
            response["item_saegw"].append(item)
            response["item_saegw_desc"] += "%s\r\n"%item_detail.name
    return jsonify(response)

@collector.route('/check', methods=['GET', 'POST'])
def check():
    wm = WorkerManager()
    data = request.get_json(True)
    ne_mme = data["ne_mme"]
    ne_saegw = data["ne_saegw"]
    item_mme = data["item_mme"]
    item_saegw = data["item_saegw"]
    check_items = get_all_modules()
    mme_modules = []
    saegw_modules = []
    for item in check_items:
        if item.id in item_mme:
            mme_modules.append(item.module)
        elif item.id in item_saegw:
            saegw_modules.append(item.module)

    dao = Dao()
    if len(mme_modules) != 0:
        for mme in ne_mme:
            ne = dao.get(str(mme))
            wm.add_worker(ne, mme_modules)
    if len(saegw_modules) != 0:
        for saegw in ne_saegw:
            ne = dao.get(str(saegw))
            wm.add_worker(ne, saegw_modules)

    result = wm.run()
    clean_old_log()
    create_new_log(result)
    zip_file = create_zip()

    return jsonify(result=result, zipfile=zip_file)

@collector.route('/download', methods=['POST'])
def download():
    filename = (request.form['filename'])
    filename = (filename.split(os.sep))[1]
    return send_from_directory('tmp', filename=filename, as_attachment=True, attachment_filename=filename)

@collector.route('/sendmail', methods=['POST'])
def sendmail():
    data = request.get_json(True)
    filename = data["filename"]
    content_name = (filename.split(os.sep))[1]

    msg = MIMEMultipart()
    attach = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
    attach["Content-Type"] = 'application/octet-stream'
    attach["Content-Disposition"] = 'attachment; filename=' + '=?utf-8?b?' + base64.b64encode(content_name.encode('UTF-8')) + '?='
    msg.attach(attach)

    msg['to'] = sc_globals.MAIL_TO
    msg['subject'] = sc_globals.MAIL_SUBJECT
    if len(msg['to']) is 0 or len(msg['subject']) is 0:
        return jsonify(success=False)

    try:
        setting_dao = SettingDao()
        msg['from'] = setting_dao.get_mailuser()
        msg['reply-to'] = setting_dao.get_email()
        server = smtplib.SMTP()
        server.connect(setting_dao.get_mailserver())
        server.login(setting_dao.get_mailuser(), setting_dao.get_mailpasswd())
        server.sendmail(msg['from'], msg['to'],msg.as_string())
        server.quit()
        return jsonify(success=True)
    except Exception as e:
        logging.error(e)
        return jsonify(success=False)


def clean_old_log():
    for file in os.listdir("tmp"):
        targetFile = os.path.join("tmp", file)
        if os.path.isfile(targetFile):
            os.remove(targetFile)

def create_new_log(log_info):
    for log in log_info:
        if not log['success']:
            continue
        with file("tmp%s%s.log"%(os.sep, log['name']), "w+") as f:
            f.write(log['log'])

def create_zip():
    setting_dao = SettingDao()
    project = setting_dao.get_project()
    filename = "tmp%s%s_%s.zip"%(os.sep, project, time.strftime('%Y_%m_%d_%H_%M_%S'))
    log_files =  os.listdir("tmp")
    with file(filename, "w+"):
        pass
    zip_file = zipfile.ZipFile(filename, mode="w")
    for log_file in log_files:
        zip_file.write("tmp%s%s"%(os.sep, log_file), log_file)
    return filename
