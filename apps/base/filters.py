#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django_filters
from django.db.models import Q


class BaseFilter(django_filters.rest_framework.FilterSet):
    is_delete = django_filters.BooleanFilter(field_name='is_delete', help_text='是否删除, true或者false')
    create_time_start = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='gte',
                                                      label='create_time >= ',
                                                      help_text='创建开始时间>= 如2019-08-19 00:00:00')
    create_time_end = django_filters.DateTimeFilter(field_name='create_time', lookup_expr='lte',
                                                    label='create_time <=', help_text='创建结束时间<= 如2019-08-19 23:59:59')
    update_time_start = django_filters.DateTimeFilter(field_name='update_time', lookup_expr='gte',
                                                      label='update_time >= ',
                                                      help_text='更新开始时间>= 如2019-08-19 00:00:00')
    update_time_end = django_filters.DateTimeFilter(field_name='update_time', lookup_expr='lte',
                                                    label='update_time <=', help_text='更新结束时间<= 如2019-08-19 23:59:59')


class UidBaseFilter(BaseFilter):
    create_user = django_filters.CharFilter(field_name='create_user', method='cu_user_ilike_filter',
                                            help_text='创建用户username模糊搜索')
    update_user = django_filters.CharFilter(field_name='updata_user', method='cu_user_ilike_filter',
                                            help_text='更新用户username模糊搜索')

    def cu_user_ilike_filter(self, queryset, name, value):
        if name == 'create_user':
            return queryset.filter(Q(create_user__username__icontains=value))
        elif name == 'update_user':
            return queryset.filter(Q(update_user__username__icontains=value))
        else:
            return queryset
