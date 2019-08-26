#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/5 11:10
# @Author  : zhe
# @Email   : huazhaozhe@outlook.com
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from operation_record import views

router = DefaultRouter()
router.register('request', views.RequestRecordViewSet)
router.register('instance', views.InstanceRecordViewSet)
router.register('field', views.InstanceFieldRecordViewSet)

urlpatterns = [
    path('get_instance_record/', views.get_instance_record_view),
    path('', include(router.urls)),
]

