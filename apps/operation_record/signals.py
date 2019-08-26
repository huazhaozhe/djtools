#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 10:04
# @Author  : zhe
# @Email   : huazhaozhe@outlook.com
# @Site    : 
# @File    : signals.py
# @Software: PyCharm


import time
from collections import OrderedDict
from copy import deepcopy

from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver

from base.middleware.globals import global_request, global_g
from base.signals import request_context_push, request_context_pop
from operation_record.models import RequestRecord, InstanceRecord, InstanceFieldRecord
from operation_record.utils.make_reocrd import make_request_record, make_model_record, make_model_field_record, \
    make_m2m_field_record, save_record


@receiver(post_save, dispatch_uid='post_save_uid')
def post_save_signal_handler(sender, **kwargs):
    if sender not in [RequestRecord, InstanceRecord, InstanceFieldRecord]:
        instance = kwargs['instance']
        mod_d = make_model_record(instance, instance_method='created' if kwargs['created'] else 'update')
        ext_mod_d = None
        if kwargs['created']:
            fie_d = make_model_field_record(instance, 'created')
        else:
            fie_d = make_model_field_record(instance, 'update')
            if hasattr(instance, '_changed_fields') and 'is_delete' in instance._changed_fields:
                instance_method = None
                if instance._changed_fields['is_delete']['old'] is False and instance._changed_fields['is_delete'][
                    'new'] is True:
                    instance_method = 'logically_delete'
                elif instance._changed_fields['is_delete']['old'] is True and instance._changed_fields['is_delete'][
                    'new'] is False:
                    instance_method = 'logically_recover'
                if instance_method is not None:
                    ext_mod_d = deepcopy(mod_d)
                    ext_mod_d['fie_d'] = []
                    ext_mod_d['instance_method'] = instance_method
        if global_g is not None and hasattr(global_g, 'operation_record'):
            instance_id = mod_d['table_name'] + '_' + str(mod_d['instance_id'])
            if instance_id not in global_g.operation_record['mod_d']:
                mod_d['fie_d'] = []
                global_g.operation_record['mod_d'][instance_id] = mod_d
            global_g.operation_record['mod_d'][instance_id]['fie_d'] += fie_d
            if ext_mod_d:
                global_g.operation_record['mod_d'][instance_id + '_' + str(time.time())] = ext_mod_d
        else:
            m_record = InstanceRecord(**mod_d)
            m_record.save()
            for fie in fie_d:
                fie['instance_record'] = m_record
                f_record = InstanceFieldRecord(**fie)
                f_record.save()
            if ext_mod_d:
                ext_mod_record = InstanceRecord(**ext_mod_d)
                ext_mod_record.save()


@receiver(m2m_changed, dispatch_uid='m2m_changed_uid')
def m2m_changed_signal_handler(sender, **kwargs):
    # ref https://docs.djangoproject.com/zh-hans/2.2/ref/signals/#django.db.models.signals.m2m_changed
    if sender not in [RequestRecord, InstanceRecord, InstanceFieldRecord]:
        mod_d = make_model_record(kwargs['instance'], instance_method='update')
        record = make_m2m_field_record(sender, **kwargs)
        if global_g is not None and hasattr(global_g, 'operation_record'):
            instance_id = mod_d['table_name'] + '_' + str(mod_d['instance_id'])
            if instance_id not in global_g.operation_record['mod_d']:
                mod_d['fie_d'] = []
                global_g.operation_record['mod_d'][instance_id] = mod_d
            if record:
                global_g.operation_record['mod_d'][instance_id]['fie_d'].append(record)
        else:
            m_record = InstanceRecord(**mod_d)
            m_record.save()
            if record:
                record['instance_record'] = m_record
                f_record = InstanceFieldRecord(**record)
                f_record.save()


@receiver(post_delete, dispatch_uid='post_delete_uid')
def post_delete_signal_handler(sender, **kwargs):
    if sender not in [RequestRecord, InstanceRecord, InstanceFieldRecord]:
        instance = kwargs['instance']
        mod_d = make_model_record(instance, instance_method='delete')
        if global_g is not None and hasattr(global_g, 'operation_record'):
            instance_id = mod_d['table_name'] + '_' + str(mod_d['instance_id']) + '_delete'
            if instance_id not in global_g.operation_record['mod_d']:
                mod_d['fie_d'] = []
                global_g.operation_record['mod_d'][instance_id] = mod_d
        else:
            m_record = InstanceRecord(**mod_d)
            m_record.save()


@receiver(request_context_push, dispatch_uid='request_context_push_uid')
def request_context_push_handler(sender, **kwargs):
    if not hasattr(global_g, 'operation_record'):
        global_g.operation_record = make_request_record(global_request)
        global_g.operation_record['mod_d'] = OrderedDict()


@receiver(request_context_pop, dispatch_uid='request_context_pop_uid')
def request_context_pop_handler(sender, **kwargs):
    if global_g is not None and hasattr(global_g, 'operation_record'):
        save_record(global_g.operation_record)
