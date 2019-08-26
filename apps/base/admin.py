from django.contrib import admin


# Register your models here.


class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_delete', 'create_time', 'update_time')

    def get_queryset(self, request):
        qs = self.model.objects.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
