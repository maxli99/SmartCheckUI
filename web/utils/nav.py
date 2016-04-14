# -*- coding: utf-8 -*-
def get_nav():
    nav = [
        {
            "name" : u"日志收集",
            "icon" : "stethoscope",
            "hidden": 0,
            "sub" : [
                {
                    "name" : u"测试",
                    "icon" : "magnet",
                    "hidden": 0,
                    "link" : "/test"
                },
                {
                    "name" : u"测试",
                    "icon" : "magic",
                    "hidden": 0,
                    "link" : "/test"
                }
            ]
        },
        {
            "name" : u"网元配置",
            "icon" : "wrench",
            "hidden": 0,
            "link" : "/config",
        },
        {
            "name" : u"测试",
            "icon" : "lightbulb",
            "hidden": 0,
            "link" : "/test"
        }
    ]

    return nav
