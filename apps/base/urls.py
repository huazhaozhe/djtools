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

from base import views

router = DefaultRouter()
router.register('user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
