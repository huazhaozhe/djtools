from django.apps import AppConfig


class OperationRecordConfig(AppConfig):
    name = 'operation_record'
    verbose_name = '操作日志'

    def ready(self):
        import operation_record.signals
