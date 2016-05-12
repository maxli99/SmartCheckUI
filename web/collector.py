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
        "ne_mme_desc" : [],
        "item_mme_desc" : [],
        "ne_saegw_desc" : [],
        "item_saegw_desc" : [],
        "item_mme_cmd" : [],
        "item_saegw_cmd" : [],
    }
    dao = Dao()
    for ne in nes:
        if not nes[ne]:
            continue
        ne_detail = dao.get(int(ne))
        if ne_detail.type == "MME":
            response["ne_mme"].append(ne)
            response["ne_mme_desc"].append(ne_detail.name)
        if ne_detail.type == "SAEGW":
            response["ne_saegw"].append(ne)
            response["ne_saegw_desc"].append(ne_detail.name)

    for item in items:
        if not items[item]:
            continue
        item_detail = get_module(str(item))
        if item_detail.type == "flexins":
            response["item_mme"].append(item)
            response["item_mme_desc"].append(item_detail.name)
            for command in item_detail.module.check_commands:
                if len(command) > 1:
                    response["item_mme_cmd"].append([command[0], command[1]])
                else:
                    response["item_mme_cmd"].append([command[0], ""])

        if item_detail.type == "flexing":
            response["item_saegw"].append(item)
            response["item_saegw_desc"].append(item_detail.name)
            for command in item_detail.module.check_commands:
                if len(command) > 1:
                    response["item_saegw_cmd"].append([command[0], command[1]])
                else:
                    response["item_saegw_cmd"].append([command[0], ""])
    return jsonify(response)

@collector.route('/check', methods=['GET', 'POST'])
def check():
    wm = WorkerManager()
    post_data = request.get_json(True)
    data = post_data["check_data"]
    mme_command = post_data["mme_command"]
    saegw_command = post_data["saegw_command"]
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
    if len(mme_command) != 0:
        for mme in ne_mme:
            ne = dao.get(str(mme))
            wm.add_worker(ne, mme_command)
    if len(saegw_command) != 0:
        for saegw in ne_saegw:
            ne = dao.get(str(saegw))
            wm.add_worker(ne, saegw_command)

    result = wm.run()
    clean_old_log()
    create_new_log(result)
    zip_file = create_zip(result)

    return jsonify(result=result, zipfile=zip_file)

@collector.route('/download', methods=['POST'])
def download():
    filename = (request.form['filename'])
    filename = (filename.split(os.sep))[1]
    return send_from_directory('tmp', filename=filename, as_attachment=True, attachment_filename=filename)

@collector.route('/sendmail', methods=['POST'])
def sendmail():
    data = request.get_json(True)
    mme_filename = data["filename"]['mme_log_zip']
    saegw_filename = data["filename"]['saegw_log_zip']
    mme_msg = None
    saegw_msg = None
    if mme_filename:
        mme_content_name = (mme_filename.split(os.sep))[1]
        mme_msg = MIMEMultipart()
        mme_attach = MIMEText(open(mme_filename, 'rb').read(), 'base64', 'utf-8')
        mme_attach["Content-Type"] = 'application/octet-stream'
        mme_attach["Content-Disposition"] = 'attachment; filename=' + '=?utf-8?b?' + base64.b64encode(mme_content_name.encode('UTF-8')) + '?='
        mme_msg.attach(mme_attach)
    if saegw_filename:
        saegw_content_name = (saegw_filename.split(os.sep))[1]
        saegw_msg = MIMEMultipart()
        saegw_attach = MIMEText(open(saegw_filename, 'rb').read(), 'base64', 'utf-8')
        saegw_attach["Content-Type"] = 'application/octet-stream'
        saegw_attach["Content-Disposition"] = 'attachment; filename=' + '=?utf-8?b?' + base64.b64encode(saegw_content_name.encode('UTF-8')) + '?='
        saegw_msg.attach(saegw_attach)

    try:
        setting_dao = SettingDao()
        server = smtplib.SMTP()
        server.connect(setting_dao.get_mailserver())
        server.login(setting_dao.get_mailuser(), setting_dao.get_mailpasswd())
        mail_from = setting_dao.get_mailuser()
        mail_to = [sc_globals.MAIL_TO, str(setting_dao.get_email())]
        if mme_filename:
            mme_msg['from'] = mail_from
            mme_msg['to'] = ",".join(mail_to)
            mme_msg['subject'] = sc_globals.MME_MAIL_SUBJECT
            server.sendmail(mail_from, mail_to, mme_msg.as_string())

        if saegw_filename:
            saegw_msg['from'] = mail_from
            saegw_msg['to'] = ",".join(mail_to)
            saegw_msg['subject'] = sc_globals.SAEGW_MAIL_SUBJECT
            server.sendmail(mail_from, mail_to, saegw_msg.as_string())

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
            f.close()

def create_zip(log_info):
    setting_dao = SettingDao()
    project = setting_dao.get_project()
    create_mme_zip = False
    create_saegw_zip = False
    for log in log_info:
        if log["type"] == "MME" and log["success"]:
            create_mme_zip = True
            break
    for log in log_info:
        if log["type"] == "SAEGW" and log["success"]:
            create_saegw_zip = True

    mme_filename = None
    saegw_filename = None
    mme_zip_file = None
    saegw_zip_file = None
    if create_mme_zip:
        mme_filename = "tmp%s%s_MMElog_%s.zip"%(os.sep, project, time.strftime('%Y_%m_%d_%H_%M_%S'))
        with file(mme_filename, "w+"):
            pass
        mme_zip_file = zipfile.ZipFile(mme_filename, mode="w")
    if create_saegw_zip:
        saegw_filename = "tmp%s%s_SAEGWlog_%s.zip"%(os.sep, project, time.strftime('%Y_%m_%d_%H_%M_%S'))
        with file(saegw_filename, "w+"):
            pass
        saegw_zip_file = zipfile.ZipFile(saegw_filename, mode="w")

    for log in log_info:
        if log["type"] == "MME" and log["success"]:
            mme_zip_file.write("tmp%s%s.log"%(os.sep, log['name']), "%s.log"%(log['name']))
        if log["type"] == "SAEGW" and log["success"]:
            saegw_zip_file.write("tmp%s%s.log"%(os.sep, log['name']), "%s.log"%(log['name']))

    if create_mme_zip:
        mme_zip_file.close()
    if create_saegw_zip:
        saegw_zip_file.close()
    return {"mme_log_zip": mme_filename, "saegw_log_zip": saegw_filename}
