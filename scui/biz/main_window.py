# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtNetwork

from scui.ui import main_ui
from scui.biz import downloader

from utils.sc_globals import sc_globals

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = main_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()

        self.web_page = self.ui.webView.page()
        self.downloader = downloader.Downloader(self, self.web_page.networkAccessManager())
        self.web_frame = self.web_page.mainFrame()

        self.web_page.setForwardUnsupportedContent(True)
        self.web_page.unsupportedContent.connect(self.downloader.saveFile)
        self.web_page.downloadRequested.connect(self.downloader.startDownload)

        self.start_browser()

    def start_browser(self):
        cookie_jar = QtNetwork.QNetworkCookieJar()
        self.web_page.networkAccessManager().setCookieJar(cookie_jar)

        self.ui.webView.load(QtCore.QUrl("http://%s:%d" % (sc_globals.LOCAL_ADDRESS, sc_globals.LOCAL_PORT)))
        self.ui.webView.show()
