#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/5 11:02
# @Author  : zhe
# @Email   : huazhaozhe@outlook.com
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers

from operation_record.models import RequestRecord, InstanceRecord, InstanceFieldRecord


class RequestRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = RequestRecord
        fields = '__all__'


class ModelRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = InstanceRecord
        fields = '__all__'


class ModelFieldRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = InstanceFieldRecord
        fields = '__all__'
