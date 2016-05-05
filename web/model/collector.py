# -*- coding: utf-8 -*-
import os
from importlib import import_module

class CheckModule(object):

    def __init__(self, id, name, type, cond, desc, oper, module):
        self.id = id
        self.name = name
        self.type = type
        self.cond = cond
        self.desc = desc
        self.module = module
        self.oper = ""
        for op in oper:
            if len(op) == 2:
                self.oper += "#%s\r\n%s\r\n" % (op[1], op[0])
            elif len(op) == 1:
                self.oper += "%s\r\n"%op[0]

def get_all_modules():
    modules = []
    embeded_sc_path = ".%ssc" % (os.sep)
    for type in ("flexins", "flexing"):
        path = "modules%s%s" %(os.sep, type)
        fns = os.listdir("%s%s%s" % (embeded_sc_path, os.sep, path))
        for name in fns:
            if name.endswith('.py') and not name.startswith('__init__'):
                mpath = '.'.join(os.path.split(path))
                mname = '.'.join([mpath,name[:-3]])
                module = import_module(mname)
                modules.append(CheckModule(module.module_id, module.name, type, module.criteria, module.desc, module.check_commands, module))
            elif os.path.isdir(os.path.join(path,name)):
                # this name is a directory.
                continue
    return modules

def get_modules(current, rowcount, search):
    result = []
    total = 0
    modules = get_all_modules()
    if len(search) != 0:
        modules = filter(lambda x: x.name.find(search) != -1 or x.type.find(search) != -1, modules)
    total = len(modules)
    offset = (int(current) - 1) * int(rowcount)
    curr = int(rowcount)
    for module in modules:
        if offset != 0:
            offset = offset - 1
            continue
        if curr == 0:
            break
        result.append(module)
        curr = curr - 1
    return result, total

def get_module(id):
    modules = get_all_modules()
    for module in modules:
        if module.id == str(id):
            return module
    return None
