#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 14:16
# @Author  : zhe
# @Email   : huazhaozhe@outlook.com
# @Site    : 
# @File    : make_reocrd.py
# @Software: PyCharm

from urllib.request import unquote

from rest_framework.utils import model_meta

from operation_record.models import RequestRecord, InstanceRecord, InstanceFieldRecord


def make_request_record(request):
    return {
        'http_method': request.method,
        'request_path': unquote(request.get_full_path()),
        'ip_address': request.META['REMOTE_ADDR'],
        'user_agent': request.META['HTTP_USER_AGENT'],
    }


def make_model_record(instance, instance_method='update', msg=''):
    return {
        'app_label': instance._meta.app_label,
        'model_verbose_name': instance._meta.verbose_name_raw,
        'model_name': instance._meta.model_name,
        'class_name': instance._meta.object_name,
        'table_name': instance._meta.db_table,
        'instance_id': getattr(instance, instance._meta.pk.attname),
        'instance_method': instance_method,
        'msg': msg
    }


def make_model_field_record(instance, method='update'):
    info = model_meta.get_field_info(instance._meta.model)
    field_list = []
    value_dict = {}
    if method == 'update' and hasattr(instance, '_changed_fields'):
        value_dict = instance._changed_fields
    elif method == 'created':
        for k, v in instance.__dict__.items():
            if k not in ['_state', '_changed_fields']:
                value_dict[k] = {
                    'old': None,
                    'new': v
                }
    for name, value in value_dict.items():
        # if not isinstance(value['old'], (str, int, float, dict, list, type(None))) or \
        #         not isinstance(value['new'], (str, int, float, dict, list, type(None))):
        #     continue
        # if name in ['create_time', 'update_time', 'create_user', 'create_user_id', 'update_user', 'update_user_id']:
        #     continue
        try:
            before_value = str(value['old'])
            after_value = str(value['new'])
        except:
            continue
        if name in info.fields:
            field_column = info.fields[name].column
            field_verbose_name = info.fields[name].verbose_name
        elif name in info.relations:
            field_column = info.relations[name].model_field.column
            field_verbose_name = info.relations[name].model_field.verbose_name
        else:
            field_column = ''
            field_verbose_name = ''
        val = {
            'field_name': name,
            'field_column': field_column,
            'field_verbose_name': field_verbose_name,
            'before_value': before_value,
            'after_value': after_value,
        }
        field_list.append(val)
    return field_list


def make_m2m_field_record(sender, **kwargs):
    record = {}
    instance = kwargs['instance']
    model = kwargs['model'] if kwargs['reverse'] else instance._meta.model
    info = model_meta.get_field_info(model)
    val_name = None
    for k in info.forward_relations:
        field = getattr(model, k)
        through = getattr(field, 'through', None)
        if through is sender:
            val_name = field.rel.related_name if kwargs['reverse'] else k
            break
    if val_name:
        field = getattr(instance, val_name)
        value = str([res.id for res in field.all()])
        field_verbose_name = '' if kwargs['reverse'] else getattr(model, val_name).field.verbose_name
        record['field_name'] = val_name
        record['field_verbose_name'] = field_verbose_name
        key = 'before_value' if kwargs['action'].startswith('pre_') else 'after_value'
        record[key] = value
        record['msg'] = kwargs['action']
    return record


def save_record(req_d):
    req_mod = req_d.pop('mod_d')
    req_r = RequestRecord(**req_d)
    req_r.save()
    for k, mod_d in req_mod.items():
        mod_fie = mod_d.pop('fie_d')
        mod_d['request_record'] = req_r
        mod_r = InstanceRecord(**mod_d)
        mod_r.save()
        for fie_d in mod_fie:
            fie_d['instance_record'] = mod_r
            fie_r = InstanceFieldRecord(**fie_d)
            fie_r.save()
