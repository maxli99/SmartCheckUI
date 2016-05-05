# -*- coding: utf-8 -*-
import logging

from web.widget.base_dao import BaseDAO
from utils.sc_globals import sc_globals

db = sc_globals.DB

class Setting(db.Model):
    __tablename__ = "SETTING"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(30))
    value = db.Column(db.String(120))

    def __init__(self, key, value):
        self.key = key
        self.value = value

class Dao(BaseDAO):
    def __init__(self):
        super(Dao, self).__init__(db, Setting)

    def get_email(self):
        return Setting.query.filter_by(key="email").first().value

    def get_project(self):
        return Setting.query.filter_by(key="project").first().value

    def get_mailuser(self):
        return Setting.query.filter_by(key="mailuser").first().value

    def get_mailpasswd(self):
        return Setting.query.filter_by(key="mailpasswd").first().value

    def get_mailserver(self):
        return Setting.query.filter_by(key="mailserver").first().value

def is_initiated():
    dao = Dao()
    try:
        settings = dao.getall()
        for setting in settings:
            if setting.key == 'project' and len(setting.value) == 0:
                return False
            if setting.key == 'email' and len(setting.value) == 0:
                return False
    except Exception as e:
        logging.error(e)
        return False
    return True

