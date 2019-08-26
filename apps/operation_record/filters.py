#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django_filters
from django.db.models import Q

from base.filters import UidBaseFilter
from operation_record.models import RequestRecord, InstanceRecord, InstanceFieldRecord


class RequestRecordFilter(UidBaseFilter):
    http_method = django_filters.CharFilter(field_name='http_method', help_text="请求方法搜索(大写)")
    request_path = django_filters.CharFilter(field_name='request_path', help_text='请求路径模糊搜索', lookup_expr='icontains')
    ip_address = django_filters.CharFilter(field_name='ip_address', help_text='ip地址模糊搜索', lookup_expr='icontains')
    user_agent = django_filters.CharFilter(field_name='user_agent', help_text='user agent模糊搜索', lookup_expr='icontains')
    include_req_record = django_filters.BooleanFilter(method='include_req_record_filter', help_text='是否包括Record记录')

    def include_req_record_filter(self, queryset, name, value=False):
        if value is False:
            return queryset.exclude(Q(request_path__istartswith='/operation_record/'))
        return queryset

    class Meta:
        model = RequestRecord
        fields = '__all__'


class InstanceRecordFilter(UidBaseFilter):
    request_record = django_filters.CharFilter(field_name='request_record', help_text='请求ID搜索')
    model_verbose_name = django_filters.CharFilter(field_name='model_verbose_name', help_text='模型中文名称搜索',
                                                   lookup_expr='icontains')

    class Meta:
        model = InstanceRecord
        fields = '__all__'


class InstanceFieldRecordFilter(UidBaseFilter):
    table_name = django_filters.CharFilter(method='table_name_filter', help_text='table_name名称搜索')
    instance_id = django_filters.CharFilter(method='instance_id_filter', help_text='instance_id搜索')
    field_verbose_name = django_filters.CharFilter(field_name='field_verbose_name', help_text='字段中文名称模糊搜索',
                                                   lookup_expr='icontains')
    before_value = django_filters.CharFilter(field_name='before_value', help_text='更改之前的值模糊搜索', lookup_expr='icontains')
    after_value = django_filters.CharFilter(field_name='after_value', help_text='更改之后的值模糊搜索', lookup_expr='icontains')

    def table_name_filter(self, queryset, name, value):
        return queryset.filter(Q(model_record__table_name=value))

    def instance_id_filter(self, queryset, name, value):
        return queryset.filter(Q(model_record__instance_id=value))

    class Meta:
        model = InstanceFieldRecord
        fields = '__all__'
