#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 15:36
# @Author  : zhe
# @Email   : huazhaozhe@outlook.com
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers

from base.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
