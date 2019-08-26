#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/15 15:54
# @Author  : zhe
# @Email   : huazhaozhe@outlook.com
# @Site    : 
# @File    : permissions.py
# @Software: PyCharm


from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsSuperUserOrAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_superuser or
                                                                        request.method in SAFE_METHODS))
