#!/usr/bin/env python
# -*- coding:utf-8 -*-

#this is a trick to let the pyqt and flask work well
#please do not change anything unless u know what u'r donging
from utils.sc_globals import sc_globals, sc_globals_editable
sc_globals_editable.QT_CLIENT = True
from bootstrap import initialize
initialize()
import webprocess
#end

import sys
import threading
import socket
import time

from PyQt4 import QtGui

from scui.biz import main_window

class WebProcess(threading.Thread):
    def __init__(self):
        super(WebProcess, self).__init__()

    def run(self):
        #sc_globals.APP.run(host=sc_globals.LOCAL_ADDRESS, port=sc_globals.LOCAL_PORT)
        sc_globals.APP.run(host="0.0.0.0", port=sc_globals.LOCAL_PORT)

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
