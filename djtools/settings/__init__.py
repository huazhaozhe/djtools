#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 14:42
# @Author  : zhe
# @Email   : huazhaozhe@outlook.com
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm

import getopt
import sys

settings_str = 'djtools.settings.base'

flag = False
for option in sys.argv:
    if '--settings' in option:
        op, val = getopt.getopt(sys.argv[sys.argv.index(option):], '', ['settings=', ])
        for name, value in op:
            settings_str = value
            flag = True
            break
    if flag:
        break

print('\n' + '=' * 50 + '\n')
print('使用settings配置: %s' % settings_str)
print('\n' + '=' * 50 + '\n')
