# -*- coding: utf-8 -*-
import sys, os

path = sys.path[0]
if os.path.isdir(path):
    os.chdir("%s%s.."%(path, os.sep))
elif os.path.isfile(path):
    os.chdir("%s%s.."%(os.path.dirname(path), os.sep))
sys.path.insert(0, ".")
import bootstrap
bootstrap.initialize()

from web.model.setting import db, Dao, Setting
db.create_all()
dao = Dao()
dao.add(Setting("email", ""))
dao.add(Setting("project", ""))
dao.add(Setting("mailuser", "smartcheckerui@sina.com"))
dao.add(Setting("mailpasswd", "Llysc1S!kr"))
dao.add(Setting("mailserver", "smtp.sina.com"))
from web.model.ne import db
db.create_all()


