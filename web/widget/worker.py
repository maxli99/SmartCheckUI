# -*- coding: utf-8 -*-

import threading
import logging

from Exscript import Account
from web.widget.connector import MMETelnet, MMESSH2, SaegwTelnet, SaegwSSH2

class Worker(threading.Thread):
    def __init__(self, ne_name, ne_id, address, port, account, conn, module_list, func):
        threading.Thread.__init__(self)
        self.ne_name = ne_name
        self.ne_id = ne_id
        self.address = address
        self.port = port
        self.account = account
        self.module_list = module_list
        self.conn = conn
        self.func = func
        self.log = ""

    def run(self):
        try:
            self.conn.connect(self.address, self.port)
            self.conn.login(self.account)
            self.log += self.conn.response
            status = True
            for module in self.module_list:
                tmp_status = True
                tmp_log, tmp_status = module.get_log(self.conn)
                self.log = self.log+tmp_log
                if tmp_status is False:
                    status = False
            self.func(self.ne_name, self.log, status, self.ne_id)
            self.conn.logout()
            self.conn.close()
        except Exception as e:
            logging.error(e)
            self.func(self.ne_name, "error happened when collecting logs\r\n", False, self.ne_id)

class WorkerManager(object):
    def __init__(self):
        super(WorkerManager, self).__init__()
        self.workers_pool = []
        self.result = []
        self.lock = threading.Lock()

    def result_callback(self, name, log, status, id):
        self.lock.acquire()
        self.result.append({"name": name, "log": log, "success": status, "id":id})
        self.lock.release()

    def add_worker(self, ne, module_list):
        conn = None
        try:
            account = Account(name=ne.user, password=ne.password)
            if ne.type == "MME":
                if ne.conntype == "Telnet":
                    conn = MMETelnet()
                elif ne.conntype == "SSH":
                    conn = MMESSH2(verify_fingerprint=False)
            elif ne.type == "SAEGW":
                if ne.conntype == "Telnet":
                    conn = SaegwTelnet()
                elif ne.conntype == "SSH":
                    conn = SaegwSSH2(verify_fingerprint=False)
            if conn == None:
                raise Exception("Unsupported NE type [%s] or connection type [%s]."%(ne.type, ne.conntype))
            worker = Worker(ne.name, ne.id, ne.address, int(ne.port), account, conn, module_list, self.result_callback)
            self.workers_pool.append(worker)
        except Exception as e:
            logging.error(e)

    def run(self):
        for worker in self.workers_pool:
            worker.start()
        for worker in self.workers_pool:
            worker.join()
        return self.result
