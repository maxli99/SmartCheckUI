# -*- coding: utf-8 -*-
def get_nav():
    nav = [
        {
            "name" : u"日志收集",
            "icon" : "stethoscope",
            "link" : "/collector",
            "hidden": 0,
        },
        {
            "name" : u"网元配置",
            "icon" : "wrench",
            "hidden": 0,
            "link" : "/ne",
        },
        {
            "name" : u"测试",
            "icon" : "lightbulb",
            "hidden": 1,
            "link" : "/test"
        }
    ]

    return nav
