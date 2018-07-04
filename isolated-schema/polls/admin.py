from django.contrib import admin

from .models import Poll, Choice

from tenants.utils import tenant_schema_from_request

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    fields = ["question", "created_by", "pub_date"]
    readonly_fields = ["pub_date"]

    def get_queryset(self, request, *args, **kwargs):
        set_tenant_schema_for_request(self.request)
        queryset = super().get_queryset(request, *args, **kwargs)
        tenant = tenant_from_request(request)
        queryset = queryset.filter(tenant=tenant)
        return queryset

    def save_model(self, request, obj, form, change):
        set_tenant_schema_for_request(self.request)
        tenant = tenant_from_request(request)
        obj.tenant = tenant
        super().save_model(request, obj, form, change)


admin.site.register(Choice)
