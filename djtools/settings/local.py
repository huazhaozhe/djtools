#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 14:55
# @Author  : zhe
# @Email   : huazhaozhe@outlook.com
# @Site    : 
# @File    : local.py
# @Software: PyCharm

from djtools.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'password',
        'NAME': 'djtools',
    },
}
