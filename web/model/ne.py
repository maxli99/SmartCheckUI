# -*- coding: utf-8 -*-
from web.widget.base_dao import BaseDAO
from utils.sc_globals import sc_globals
from sqlalchemy import or_

db = sc_globals.DB

class NE(db.Model):
    __tablename__ = "NE"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.String(16))
    conntype = db.Column(db.String(16))
    address = db.Column(db.String(64))
    port = db.Column(db.Integer)
    user = db.Column(db.String(64))
    password = db.Column(db.String(64))

    def __init__(self, name, type, conntype, address, port, user, password):
        self.name     =  name
        self.type     = type
        self.conntype = conntype
        self.address  = address
        self.port     = port
        self.user     = user
        self.password = password

class Dao(BaseDAO):
    def __init__(self):
        super(Dao, self).__init__(db, NE)

    def get_page(self, curr, pagecount, filter, order_type, order_column):
        return NE.query.filter(or_("name like '%%%s%%'"%(filter), "address like '%%%s%%'"%(filter)))\
            .order_by("%s %s"%(order_column, order_type)).offset(pagecount*(curr-1)).limit(pagecount).all()

    def get_total(self):
        return NE.query.count()
