from django.db import models

from base.models import UidBaseModel


# Create your models here.


class RequestRecord(UidBaseModel):
    http_method = models.CharField(verbose_name='HTTP METHOD', max_length=64, blank=True)
    request_path = models.TextField(verbose_name='请求的path', blank=True)
    ip_address = models.CharField(verbose_name='IP地址', max_length=40, blank=True)
    user_agent = models.TextField(verbose_name='UA', blank=True)

    class Meat:
        verbose_name = '操作日志请求记录表'
        verbose_name_plural = verbose_name


class InstanceRecord(UidBaseModel):
    request_record = models.ForeignKey(RequestRecord, verbose_name='请求记录', on_delete=models.SET_NULL, null=True,
                                       blank=True)
    app_label = models.CharField(verbose_name='app_label', max_length=64, blank=True)
    model_verbose_name = models.CharField(verbose_name='模型verbose_name', max_length=128, blank=True)
    model_name = models.CharField(verbose_name='模型名称', max_length=128, blank=True)
    class_name = models.CharField(verbose_name='模型class名称', max_length=128, blank=True)
    table_name = models.CharField(verbose_name='数据库表名称', max_length=128, blank=True)
    instance_id = models.CharField(verbose_name='记录的主键', max_length=255, blank=True)
    instance_method = models.CharField(verbose_name='操作方法', max_length=64, blank=True)
    msg = models.TextField(verbose_name='备注', blank=True)

    class Meta:
        verbose_name = '操作日志模型记录表'
        verbose_name_plural = verbose_name


class InstanceFieldRecord(UidBaseModel):
    instance_record = models.ForeignKey(InstanceRecord, verbose_name='操作记录', on_delete=models.CASCADE)
    field_name = models.CharField(verbose_name='字段名称', max_length=64, blank=True)
    field_verbose_name = models.CharField(verbose_name='verbose_name', max_length=128, blank=True)
    field_column = models.CharField(verbose_name='数据库字段名', max_length=128, blank=True)
    before_value = models.CharField(verbose_name='前一个值', max_length=255, blank=True)
    after_value = models.CharField(verbose_name='更新的值', max_length=255, blank=True)
    msg = models.TextField(verbose_name='备注', blank=True)

    class Meta:
        verbose_name = '操作日志字段记录表'
        verbose_name_plural = verbose_name
