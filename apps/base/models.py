# -*- coding: utf-8 -*-

from copy import deepcopy

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import FieldDoesNotExist
from django.db import models

from base.middleware.globals import global_request


class InstanceChangedFieldsMixin(object):
    '''
    Model对象添加_changed_fields属性, 用于跟踪实例值的变化
    '''

    def __init__(self, *args, **kwargs):
        super(InstanceChangedFieldsMixin, self).__init__(*args, **kwargs)

        self._changed_fields = {}  # 初始化字典，用户存储字段变更的信息

    def __setattr__(self, name, value):
        '''
        重写__setattr__方法用于对属性赋值检测
        '''

        if hasattr(self, '_changed_fields'):
            try:
                field = self._meta.get_field(name)  # 通过属性名称获取field对象，如果不是field属性则忽略
            except FieldDoesNotExist:
                field = None
            if field and not (field.auto_created or field.hidden) and field.__class__ not in (
                    models.ManyToManyField, models.ManyToOneRel):  # 如果不是自动创建，隐藏字段，多对多，多对一的关联对象
                try:
                    old = getattr(self, name, FieldDoesNotExist)  # 获取赋值前的属性值
                except field.rel.to.DoesNotExist:
                    old = FieldDoesNotExist

                super(InstanceChangedFieldsMixin, self).__setattr__(name, value)  # 赋值
                new = getattr(self, name, FieldDoesNotExist)  # 获取新的属性值
                try:
                    changed = (old != new)  # 比较
                except:
                    changed = True
                if changed:  # 如果发现值变更了
                    self._changed_fields[name] = {
                        'old': deepcopy(old),
                        'new': new,
                    }
                elif self.id is None:
                    self._changed_fields[name] = {
                        'new': new,
                    }
            else:
                super(InstanceChangedFieldsMixin, self).__setattr__(name, value)
        else:
            super(InstanceChangedFieldsMixin, self).__setattr__(name, value)

    # def save(self, *args, **kwargs):
    #     '''
    #     重写save方法，传update_fields参数
    #     '''
    #     if not self._state.adding and hasattr(self,
    #                                           '_changed_fields') and 'update_fields' not in kwargs and not kwargs.get(
    #         'force_insert', False):
    #         kwargs['update_fields'] = [key for key, value in self._changed_fields.iteritems() if hasattr(self, key)]
    #         self._changed_fields = {}
    #     return super(InstanceChangedFieldsMixin, self).save(*args, **kwargs)


class BaseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)


class IsDeletedException(Exception):
    pass


class BaseModel(models.Model, InstanceChangedFieldsMixin):
    is_delete = models.BooleanField(verbose_name='是否删除', default=False, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True, null=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True, blank=True, null=True)

    objects = models.Manager()

    existent = BaseManager()

    def __str__(self):
        return '-'.join([str(self.__class__), str(self.id), str(self.is_delete)])

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        if kwargs.get('real_delete', False):
            return super().delete(using=using, keep_parents=keep_parents)
        if self.is_delete:
            raise IsDeletedException('记录 %s 已经逻辑删除!' % self.id)
        self.is_delete = True
        return self.save()

    class Meta:
        abstract = True


# 需要再settings中设置
# AUTH_USER_MODEL = 'base.User'
class User(AbstractUser, BaseModel):
    objects = UserManager()

    class Meta:
        verbose_name = "用户模型"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if global_request != None and global_request.user.is_authenticated:
            if self.id is None:
                self.create_user = global_request.user
            else:
                self.update_user = global_request.user
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)


class UidBaseModel(BaseModel):
    create_user = models.ForeignKey(User, verbose_name='创建人', related_name='%(app_label)s_%(class)s_create_user',
                                    on_delete=models.SET_NULL, null=True, blank=True, default=None)
    update_user = models.ForeignKey(User, verbose_name='修改人', related_name='%(app_label)s_%(class)s_update_user',
                                    on_delete=models.SET_NULL, null=True, blank=True, default=None)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if global_request != None and global_request.user.is_authenticated:
            if self.id is None:
                self.create_user = global_request.user
            else:
                self.update_user = global_request.user
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)
