# -*- coding: utf-8 -*-
from utils.singleton import singleton

__all__ = ["suci_globals", "scui_globals_editable"]

@singleton
class _GlobalVarEditable(object):
    _vars = {}

    def __setattr__(self, name, val):
        self._vars[name] = val

    def __getattr__(self, name):
        if name in self._vars:
            return self._vars[name]
        else:
            return None

    def get(self, name):
        return self.__getattr__(name)

@singleton
class _GlobalVar(object):
    _vars = _GlobalVarEditable()

    def __setattr__(self, name, val):
        return None

    def __getattr__(self, name):
        return self._vars.get(name)

sc_globals = _GlobalVar()
sc_globals_editable = _GlobalVarEditable()
