#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/12 11:06
# @Author  : zhe
# @Email   : huazhaozhe@outlook.com
# @Site    : 
# @File    : globals.py
# @Software: PyCharm

from functools import partial

from django.utils.deprecation import MiddlewareMixin
from werkzeug.local import LocalStack, LocalProxy

from base.signals import request_context_push, request_context_pop


def _lookup_req_object(name):
    return getattr(_request_ctx_stack.top, name, None)


_request_ctx_stack = LocalStack()
global_request = LocalProxy(partial(_lookup_req_object, 'request'))
global_g = LocalProxy(partial(_lookup_req_object, 'g'))


class _GlobalsG(object):
    pass


class _RequestContext(object):

    def __init__(self, request):
        self.request = request
        self.g = _GlobalsG()


class GlobalRequestMiddleware(MiddlewareMixin):

    # def process_request(self, request):
    #     _request_ctx_stack.push(_RequestContext(request))
    #     request_context_push.send(sender=self.__class__, func='process_request')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        _request_ctx_stack.push(_RequestContext(request))
        kw = {
            'request': request,
            'func': 'process_view',
        }
        request_context_push.send(sender=self.__class__, kw=kw)
        return None

    def process_response(self, request, response):
        kw = {
            'request': request,
            'response': response,
            'func': 'process_response'
        }
        request_context_pop.send(sender=self.__class__, kw=kw)
        _request_ctx_stack.pop()
        return response

    def process_exception(self, request, exception):
        kw = {
            'request': request,
            'exception': exception,
        }
        request_context_pop.send(sender=self.__class__, kw=kw)
        _request_ctx_stack.pop()
