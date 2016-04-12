#!/usr/bin/python2
# -*- coding:utf-8 -*-

import os
for item in os.walk('.'):
    for file in item[2]:
        if file.endswith('.ui'):
            os.system('pyuic4 -o %s%s%s.py %s%s%s' % (item[0], os.sep, file.rsplit('.', 1)[0], item[0], os.sep, file))
        elif file.endswith('.qrc'):
            os.system('pyrcc4 -o %s%s%s_rc.py %s%s%s' % (item[0], os.sep, file.rsplit('.', 1)[0], item[0], os.sep, file))
