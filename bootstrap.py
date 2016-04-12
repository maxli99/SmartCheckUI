# -*- coding: utf-8 -*-

import os
import sys

from utils.sc_globals import sc_globals_editable

__all__ = ["initialize"]

def _change_pwd(working_dir):
    os.chdir(working_dir)

def _add_lib_path(lib_path):
    sys.path.insert(0, "%s"%(lib_path))

def initialize():
    # set default charset
    reload(sys)
    sys.setdefaultencoding('utf8')

    current_dir = os.path.dirname(__file__)
    _change_pwd(current_dir)
    _add_lib_path(current_dir)
    _add_lib_path("%s%s%s" % (current_dir, os.sep, "libs"))

    sc_globals_editable.LOCAL_ADDRESS = "127.0.0.1"
    sc_globals_editable.LOCAL_PORT = 61030
    sc_globals_editable.SERVICE_PORT = 5001
    sc_globals_editable.MAX_WAIT_FOR_WEBSERVER_RETRY = 3

    sc_globals_editable.APP_NAME = "SmartCheckUI"
    sc_globals_editable.DEBUG = False
