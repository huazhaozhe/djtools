# Create your views here.

from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from base.filters import UidBaseFilter
from base.models import User, IsDeletedException
from base.serializers import UserSerializer
from base.permissions import IsSuperUser


class DefaultPagination(PageNumberPagination):
    """自定义分页"""
    # 每页显示多少条数据
    page_size = 100
    page_size_query_description = _('每页数据大小, 默认100')
    # url/?page=1&size=5, 改变默认每页显示的个数
    page_size_query_param = "pageSize"
    # 最大页数不超过10条
    max_page_size = 10
    # 获取页码数
    page_query_param = "currentPage"
    page_query_description = _('页数, 默认1')

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'page': {
                'currentPage': self.page.number,  # 当前页码
                'totalPage': self.page.paginator.num_pages,  # 总页数
                'totalRecords': self.page.paginator.count,  # 总条数
                'pageSize': self.page.paginator.per_page,  # 每一页条数
                'page_num': len(data),
                'next': self.get_next_link(),
            }
        })


class BaseAPIView(generics.GenericAPIView):
    filter_backends = (DjangoFilterBackend,)
    pagination_class = DefaultPagination
    filter_class = UidBaseFilter


class BaseGenericViewSet(viewsets.ViewSetMixin, BaseAPIView):
    pass


class BaseViewSet(BaseGenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  ):

    def destroy(self, request, *args, **kwargs):
        data = ''
        instance = self.get_object()
        if hasattr(instance, 'is_delete'):
            real_delete = kwargs.get('real_delete', False) if self.request.user.is_superuser else False
            if real_delete:
                try:
                    flag = instance.delete(real_delete=real_delete)
                except:
                    raise APIException('真实删除失败!')
            elif instance.is_delete is False:
                try:
                    flag = instance.delete()
                except IsDeletedException as e:
                    raise APIException(e)
                except:
                    raise APIException('逻辑删除失败!')
            else:
                data = '已经删除'
        else:
            try:
                instance.delete()
            except:
                raise APIException('删除失败!')
        # self.perform_destroy(instance)
        return Response(data, status=status.HTTP_200_OK)


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)
