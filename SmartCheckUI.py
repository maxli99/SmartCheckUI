#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import threading
import socket
import time

from PyQt4 import QtGui

from scui.biz import main_window
from webprocess import app as webapp
from utils.sc_globals import sc_globals

class WebProcess(threading.Thread):
    def __init__(self):
        super(WebProcess, self).__init__()

    def run(self):
        webapp.run(host=sc_globals.LOCAL_ADDRESS, port=sc_globals.LOCAL_PORT)

    def is_initiated(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((sc_globals.LOCAL_ADDRESS, sc_globals.LOCAL_PORT))
            s.shutdown(2)
            return True
        except Exception as e:
            print(e)
            return False


class MainProcess(object):
    def __init__(self, argv):
        self._argv = argv

    def run(self):
        #logging.basicConfig(level=logging.DEBUG,
        #                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        #                    datefmt='%a, %d %b %Y %H:%M:%S',
        #                    filename='%s%s%s'%(os.getcwd(), os.sep, 'FMA_Portal.log'),
        #                    filemode='a+')
        app = QtGui.QApplication(self._argv)
        ui = main_window.MainWindow()
        ui.show()
        return app.exec_()

if __name__ == '__main__':
    web_process = WebProcess()
    web_process.setDaemon(True)
    web_process.start()
    delay_count = 0
    while not web_process.is_initiated():
        if delay_count is sc_globals.MAX_WAIT_FOR_WEBSERVER_RETRY:
            sys.exit(0)
        time.sleep(1)
        delay_count += 1

    main_process = MainProcess(sys.argv)
    sys.exit(main_process.run())
