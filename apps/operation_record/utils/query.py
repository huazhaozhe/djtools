#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/23 9:23
# @Author  : zhe
# @Email   : huazhaozhe@outlook.com
# @Site    : 
# @File    : query.py
# @Software: PyCharm

from operation_record.models import RequestRecord, InstanceRecord, InstanceFieldRecord


def get_instance_record(table_name, instance_id, order_by=None):
    if order_by is None:
        order_by = ['-create_time']
    instance_record = InstanceRecord.objects.filter(table_name=table_name, instance_id=instance_id).order_by(*order_by)
    first = instance_record.first()
    record_dict = {}
    if first is not None:
        record_dict['info'] = {
            'table_name': table_name,
            'instance_id': instance_id,
            'model_name': first.model_name,
            'verbose_name': first.model_verbose_name,
        }
        record_dict['record'] = []
        for record in instance_record:
            val = {
                'create_time': record.create_time,
                'create_user': record.create_user.id if record.create_user else '',
                'create_user_name': record.create_user.username if record.create_user else '',
                'instance_method': record.instance_method,
                'request': True if record.request_record_id else False,
                'request_path': record.request_record.request_path if record.request_record else '',
                'request_method': record.request_record.http_method if record.request_record else '',
                'msg': record.msg,
            }
            record_dict['record'].append(val)
    return record_dict
