#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 13:58
# @Author  : zhe
# @Email   : huazhaozhe@outlook.com
# @Site    : 
# @File    : signals.py
# @Software: PyCharm

from django.dispatch import Signal

request_context_push = Signal(providing_args=['kw'])
request_context_pop = Signal(providing_args=['kw'])
