# Create your views here.

import coreapi
from rest_framework import status
from rest_framework.decorators import api_view, schema, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from base.permissions import IsSuperUserOrAuthenticatedReadOnly
from base.views import BaseViewSet
from operation_record.filters import RequestRecordFilter, InstanceRecordFilter, InstanceFieldRecordFilter
from operation_record.models import RequestRecord, InstanceRecord, InstanceFieldRecord
from operation_record.serializers import RequestRecordSerializers, ModelRecordSerializers, ModelFieldRecordSerializers
from operation_record.utils.query import get_instance_record


class RequestRecordViewSet(BaseViewSet):
    """
    list:
        获取符合条件的Request列表
    create:
        创建一个Request记录
    retrieve:
        得到一个Request记录的详情
    update:
        更改一个Request记录
    destroy:
        删除一个Request记录
    """
    queryset = RequestRecord.objects.all()
    serializer_class = RequestRecordSerializers
    permission_classes = (IsSuperUserOrAuthenticatedReadOnly,)
    filter_class = RequestRecordFilter

    def get_queryset(self):
        include_req_record = self.request.query_params.get('include_req_record', 'flase')
        if include_req_record == 'true':
            return RequestRecord.objects.all()
        else:
            return RequestRecord.objects.exclude(request_path__istartswith='/operation_record/').all()


class InstanceRecordViewSet(BaseViewSet):
    """
    list:
        获取符合条件的模型记录列表
    create:
        创建一个模型记录
    retrieve:
        得到一个模型记录的详情
    update:
        更改一个模型记录
    destroy:
        删除一个模型记录
    """
    queryset = InstanceRecord.objects.all()
    serializer_class = ModelRecordSerializers
    permission_classes = (IsSuperUserOrAuthenticatedReadOnly,)
    filter_class = InstanceRecordFilter


class InstanceFieldRecordViewSet(BaseViewSet):
    """
    list:
        获取符合条件的字段记录列表
    create:
        创建一个字段记录
    retrieve:
        得到一个字段记录的详情
    update:
        更改一个字段记录的信息
    destroy:
        删除一个字段记录
    """
    queryset = InstanceFieldRecord.objects.all()
    serializer_class = ModelFieldRecordSerializers
    permission_classes = (IsSuperUserOrAuthenticatedReadOnly,)
    filter_class = InstanceFieldRecordFilter


instance_record_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(name='table_name', required=True, location='query', description='表名称', type='string'),
        coreapi.Field(name='instance_id', required=True, location='query', description='实例主键值', type='string'),
    ]
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@schema(instance_record_schema)
def get_instance_record_view(request):
    '''
    获取特定实例的操作记录
    '''
    table_name = request.GET.get('table_name', None)
    instance_id = request.GET.get('instance_id', None)
    if table_name is None or instance_id is None:
        return Response({'msg': '请求参数缺失!'}, status=status.HTTP_400_BAD_REQUEST)
    record = get_instance_record(table_name=table_name, instance_id=instance_id)
    return Response(record)
