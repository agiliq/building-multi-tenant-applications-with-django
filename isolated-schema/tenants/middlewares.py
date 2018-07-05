from tenants.utils import set_tenant_schema_for_request


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_tenant_schema_for_request(request)
        response = self.get_response(request)
        return response
