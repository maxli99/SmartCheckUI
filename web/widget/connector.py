# -*- coding: utf-8 -*-

__all__ = ['MMETelnet', 'MMESSH2', 'FlexiNGTelnet', 'FlexiNGSSH2']

import re
from Exscript.protocols.drivers.driver import Driver
from Exscript.protocols.drivers import driver_map
from Exscript.protocols import Telnet,SSH2

class MMESSH2Driver(Driver):
    def __init__(self):
        Driver.__init__(self, 'mme_ssh2')

        self.password_re = [re.compile(r'password:')]
        self.prompt_re = [re.compile(r'\r\n< \x08 ')]
        self.login_error_re = [re.compile(r'Permission denied')]

    def check_head_for_os(self, string):
        if self.user_re[0].search(string):
            return 80
        if self.prompt_re[0].search(string):
            return 75
        return 0

class MMETelnetDriver(Driver):
    def __init__(self):
        Driver.__init__(self, 'mme_telnet')

        self.user_re     = [re.compile(r'ENTER USERNAME < ')]
        self.password_re = [re.compile(r'ENTER PASSWORD < ')]
        self.prompt_re = [re.compile(r'\r\n< \x08 ')]
        self.login_error_re = [re.compile(r'AUTHORIZATION FAILURE ')]

    def check_head_for_os(self, string):
        if self.user_re[0].search(string):
            return 80
        if self.prompt_re[0].search(string):
            return 75
        return 0

class SaegwTelnetDriver(Driver):
    def __init__(self):
        Driver.__init__(self, 'saegw_telnet')
        self.user_re     = [re.compile(r'Please give the username:\r\n')]
        self.password_re = [re.compile(r'Please give the password for user\r\n')]
        self.prompt_re = [re.compile(r'\[.*\][\r\x00]*\r\n#')]

    def check_head_for_os(self, string):
        if self.user_re[0].search(string):
            return 80
        if self.prompt_re[0].search(string):
            return 75
        return 0

class SaegwSSH2Driver(Driver):
    def __init__(self):
        Driver.__init__(self, 'saegw_ssh2')
        self.password_re = [re.compile(r'Password:')]
        self.prompt_re = [re.compile(r'\[.*\][\r\x00]*\r\n#')]

    def check_head_for_os(self, string):
        if self.user_re[0].search(string):
            return 80
        if self.prompt_re[0].search(string):
            return 75
        return 0


def register_drivers(*drivers):
    d_error = 0
    for d in drivers:
        #print "register driver:%s" % d.name
        try:
            driver_map[d.name] = d
        except:
            d_error +=1
    return d_error

class SaegwTelnet(Telnet):
    def __init__(self, **kwargs):
        Telnet.__init__(self, **kwargs)
        register_drivers(SaegwTelnetDriver())
        self.set_driver('saegw_telnet')

    def logout(self,cmd=None):
        if cmd:
            self.send(cmd+'\r')
        else:
            self.send('exit\r')

    def dds(self):
        "handling the DDS interact process"
        pass

class SaegwSSH2(SSH2):
    def __init__(self, **kwargs):
        SSH2.__init__(self, **kwargs)
        register_drivers(SaegwSSH2Driver())
        self.set_driver('saegw_ssh2')

    def logout(self,cmd=None):
        if cmd:
            self.send(cmd+'\r')
        else:
            self.send('exit\r')

    def dds(self):
        "handling the DDS interact process"
        pass

class MMETelnet(Telnet):
    def __init__(self, **kwargs):
        Telnet.__init__(self, **kwargs)
        register_drivers(MMETelnetDriver())
        self.set_driver('mme_telnet')

    def logout(self,cmd=None):
        if cmd:
            self.send(cmd+'\r')
        else:
            self.send('ZZZ;\r')

    def dds(self):
        "handling the DDS interact process"
        pass

class MMESSH2(SSH2):
    def __init__(self, **kwargs):
        SSH2.__init__(self, **kwargs)
        register_drivers(MMESSH2Driver())
        self.set_driver('mme_ssh2')

    def logout(self,cmd=None):
        if cmd:
            self.send(cmd+'\r')
        else:
            self.send('ZZZ;\r')

    def dds(self):
        "handling the DDS interact process"
        pass
