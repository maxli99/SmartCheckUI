# -*- coding: utf-8 -*-

import threading
import logging

from Exscript import Account
from web.widget.connector import MMETelnet, MMESSH2, SaegwTelnet, SaegwSSH2

class Worker(threading.Thread):
    def __init__(self, ne_id, ne_name, ne_type, address, port, account, conn, commands, func):
        threading.Thread.__init__(self)
        self.ne_id = ne_id
        self.ne_name = ne_name
        self.ne_type = ne_type
        self.address = address
        self.port = port
        self.account = account
        self.commands = commands
        self.conn = conn
        self.func = func
        self.log = ""

    def run(self):
        try:
            self.conn.connect(self.address, self.port)
            self.conn.login(self.account)
            self.log += self.conn.response
            status = True
            for command in self.commands:
                self.conn.execute(command)
                self.log += self.conn.response
            self.func(self.ne_name, self.ne_type, self.log, status, self.ne_id)
            self.conn.logout()
            self.conn.close()
        except Exception as e:
            logging.error(e)
            self.func(self.ne_name, self.ne_type, "error happened when collecting logs\r\n", False, self.ne_id)

class WorkerManager(object):
    def __init__(self):
        super(WorkerManager, self).__init__()
        self.workers_pool = []
        self.result = []
        self.lock = threading.Lock()

    def result_callback(self, name, type, log, status, id):
        self.lock.acquire()
        self.result.append({"name": name, "type": type, "log": log, "success": status, "id":id})
        self.lock.release()

    def add_worker(self, ne, command_list):
        if len(command_list) is 0:
            return
        commands = []
        for cmd in command_list:
            cls = cmd.split("\n")
            for cl in cls:
                cl = cl.strip()
                if len(cl) > 0:
                    commands.append(cl.strip())
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
            worker = Worker(ne.id, ne.name, ne.type, ne.address, int(ne.port), account, conn, commands, self.result_callback)
            self.workers_pool.append(worker)
        except Exception as e:
            logging.error(e)

    def run(self):
        for worker in self.workers_pool:
            worker.start()
        for worker in self.workers_pool:
            worker.join()
        return self.result
