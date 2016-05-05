# -*- coding: utf-8 -*-

import os
import sys
import logging

from utils.sc_globals import sc_globals_editable, sc_globals

__all__ = ["initialize"]

def _change_pwd(working_dir):
    os.chdir(working_dir)

def _add_lib_path(lib_path):
    sys.path.insert(0, "%s"%(lib_path))

def initialize():
    if sc_globals.INITIATED:
        return
    # set default charset
    reload(sys)
    sys.setdefaultencoding('utf8')

    current_dir = os.path.dirname(__file__)
    _change_pwd(current_dir)
    _add_lib_path(current_dir)
    _add_lib_path("%s%s%s" % (current_dir, os.sep, "libs"))
    _add_lib_path("%s%s%s" % (current_dir, os.sep, "sc"))
    _add_lib_path("%s%s%s" % (current_dir, os.sep, "extra_libs"))

    # import libs after the changing of the lib path
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    import jsoncfg
    boot_file = 'config%sboot.json' % (os.sep)
    initiated = False
    try:
        boot_config = jsoncfg.load_config(boot_file)
        sc_globals_editable.LOCAL_ADDRESS = boot_config.local_address("127.0.0.1")
        sc_globals_editable.LOCAL_PORT = boot_config.local_port(61030)
        sc_globals_editable.SERVICE_PORT = boot_config.service_port(5001)
        sc_globals_editable.MAX_WAIT_FOR_WEBSERVER_RETRY = boot_config.max_wait_for_webserver_retry(3)
        sc_globals_editable.APP_NAME = boot_config.app_name("Smart Check UI")
        sc_globals_editable.DEBUG = boot_config.debug(False)
        sc_globals_editable.DB_URL = boot_config.db_url('sqlite:///./config/config.db')
        sc_globals_editable.MAIL_TO = boot_config.mail_to('')
        sc_globals_editable.MAIL_SUBJECT = boot_config.mail_subject('')
        sc_globals_editable.LOG= boot_config.log(True)
        sc_globals_editable.LOG_FILE= boot_config.log_file('scui.log')
        sc_globals_editable.LOG_LEVEL= boot_config.log_level('INFO')
        initiated = True
    except Exception as e:
        print(e)
        pass

    if not initiated:
        sc_globals_editable.LOCAL_ADDRESS = "127.0.0.1"
        sc_globals_editable.LOCAL_PORT = 61030
        sc_globals_editable.SERVICE_PORT = 5001
        sc_globals_editable.MAX_WAIT_FOR_WEBSERVER_RETRY = 3
        sc_globals_editable.APP_NAME = "SmartCheckUI"
        sc_globals_editable.DEBUG = False
        sc_globals_editable.DB_URL = 'sqlite:///./config/config.db'
        sc_globals_editable.MAIL_TO = ''
        sc_globals_editable.MAIL_SUBJECT = ''
        sc_globals_editable.LOG= True
        sc_globals_editable.LOG_FILE= 'scui.log'
        sc_globals_editable.LOG_LEVEL= 'INFO'

    log_level = logging.DEBUG
    if sc_globals.LOG_LEVEL.lower() == 'debug':
        log_level = logging.DEBUG
    elif sc_globals.LOG_LEVEL.lower() == 'info':
        log_level = logging.INFO
    elif sc_globals.LOG_LEVEL.lower() == 'warning':
        log_level = logging.WARNING
    elif sc_globals.LOG_LEVEL.lower() == 'error':
        log_level = logging.ERROR
    elif sc_globals.LOG_LEVEL.lower() == 'critical':
        log_level = logging.CRITICAL

    logging.basicConfig(level=log_level,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename= sc_globals.LOG_FILE,
                    filemode='a+')
    if not sc_globals.LOG:
        logging.disable(logging.CRITICAL)

    app = Flask(sc_globals.APP_NAME)
    app.config['SECRET_KEY'] = 'scui'
    app.config['UPLOAD_FOLDER'] = 'tmp'
    app.config['MAX_CONTENT_LENGTH'] = 16777216

    if sc_globals.QT_CLIENT:
        app.debug = False
    else:
        app.debug = sc_globals.DEBUG

    app.use_reloader = False

    #session
    app.secret_key = '\x80p;\x05\\}\xba\x8bd\xd8\xb0M#`B\xe9\x8c\x07"\xb0Q&V\xb5"`'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = sc_globals.DB_URL

    db = SQLAlchemy(app)

    sc_globals_editable.APP = app
    sc_globals_editable.DB = db

    sc_globals_editable.INITIATED = True
