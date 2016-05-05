# -*- coding: utf-8 -*-

class BaseDAO(object):

    def __init__(self, db, model):
        super(BaseDAO, self).__init__()
        self._db = db
        self._module = model

    def get(self, id):
        return self._module.query.filter_by(id=id).first()

    def getall(self):
        return self._module.query.all()

    def update(self):
        return self._db.session.commit()

    def add(self, row):
        self._db.session.add(row)
        return self._db.session.commit()

    def remove(self, row):
        self._db.session.delete(row)
        return self._db.session.commit()

