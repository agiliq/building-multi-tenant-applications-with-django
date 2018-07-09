Shared database with shared schema
---------------------------------------

In this chapter, we will rebuild a slightly modified Django polls app to be multi-tenant.
You can download the `code from Github <https://github.com/agiliq/building-multi-tenant-applications-with-django/tree/master/base>`_.

The base single-tenant app
++++++++++++++++++++++++++++

Our base project has one app called :code:`polls`. The models look something like this.

.. code-block:: python

    from django.db import models
    from django.contrib.auth.models import User


    class Poll(models.Model):
        question = models.CharField(max_length=100)
        created_by = models.ForeignKey(User, on_delete=models.CASCADE)
        pub_date = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.question


    class Choice(models.Model):
        poll = models.ForeignKey(Poll, related_name='choices',on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=100)

        def __str__(self):
            return self.choice_text


    class Vote(models.Model):
        choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
        poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
        voted_by = models.ForeignKey(User, on_delete=models.CASCADE)

        class Meta:
            unique_together = ("poll", "voted_by")

There are a number of other files which we will look at later.

Adding multi tenancy to models
+++++++++++++++++++++++++++++++

We will add another app called :code:`tenants`

.. code-block:: bash

    python manage.py startapp tenants


Create a model for storing :code:`Tenant` data.

.. code-block:: python

    class Tenant(models.Model):
        name = models.CharField(max_length=100)
        subdomain_prefix = models.CharField(max_length=100, unique=True)

And then create a class :code:`TenantAwareModel` class which other models with subclass from.

.. code-block:: python

    class TenantAwareModel(models.Model):
        tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

        class Meta:
            abstract = True


Change the :code:`polls.models` to subclass from :code:`TenantAwareModel`.


.. code-block:: python

    # ...

    class Poll(TenantAwareModel):
        # ...


    class Choice(TenantAwareModel):
        # ...


    class Vote(TenantAwareModel):
        # ...


Identifying tenants
+++++++++++++++++++++++++++++++

There are many approaches to identify the tenant. One common method is to give each tenant their own subdomain. So if you main website is

:code:`www.example.com`

And each of the following will be a separate tenant.

- thor.example.com
- loki.example.com
- potter.example.com

We will use the same method in the rest of the book. Our :code:`Tenant` model has :code:`subdomain_prefix` which will identify the tenant.

We will use :code:`polls.local` as the main domain and :code:`<xxx>.polls.local` as tenant subdomain.


Extracting tenant from request
+++++++++++++++++++++++++++++++

Django views always have a :code:`request` which has the :code:`Host` header. This will contain the full subdomain the tenant is using.
We will add some utility methods to do this. Create a :code:`utils.py` and add this code.

.. code-block:: python

    from .models import Tenant


    def hostname_from_request(request):
        # split on `:` to remove port
        return request.get_host().split(':')[0].lower()


    def tenant_from_request(request):
        hostname = hostname_from_request(request)
        subdomain_prefix = hostname.split('.')[0]
        return Tenant.objects.filter(subdomain_prefix=subdomain_prefix).first()


Now wherever you have a :code:`request`, you can use :code:`tenant_from_request` to get the tenant.


A detour to /etc/hosts
+++++++++++++++++++++++++++++++

To ensure that the :code:`<xxx>.polls.local` hits your development machine, make sure you add a few entries to your :code:`/etc/hosts`

(If you are on windows, use :code:`C:\Windows\System32\Drivers\etc\hosts`). My file looks like this.

.. code-block:: text

     # ...
     127.0.0.1 polls.local
     127.0.0.1 thor.polls.local
     127.0.0.1 potter.polls.local

Also update :code:`ALLOWED_HOSTS` your settings.py. Mine looks like this: :code:`ALLOWED_HOSTS = ['polls.local', '.polls.local']`.


Using :code:`tenant_from_request` in the views
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Views, whether they are Django function based, class based or a Django Rest Framework view have access to the request.
Lets take the example of :code:`polls.views.PollViewSet` to limit the endpoints to tenant specific :code:`Poll` objects.

.. code-block:: python

    from tenants.utils import tenant_from_request


    class PollViewSet(viewsets.ModelViewSet):
        queryset = Poll.objects.all()
        serializer_class = PollSerializer

        def get_queryset(self):
            tenant = tenant_from_request(self.request)
            return super().get_queryset().filter(tenant=tenant)


Isolating the admin
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Like the views we need to enforce tenant isolation on the admin. We will need to override two methods.

- :code:`get_queryset`: So that only the current tenant's objects show up.
- :code:`save_model`: So that tenant gets set on the object when the object is saved.

With the changes, your :code:`admin.py` looks something like this.

.. code-block:: python

    @admin.register(Poll)
    class PollAdmin(admin.ModelAdmin):
        fields = ["question", "created_by", "pub_date"]
        readonly_fields = ["pub_date"]

        def get_queryset(self, request, *args, **kwargs):
            queryset = super().get_queryset(request, *args, **kwargs)
            tenant = tenant_from_request(request)
            queryset = queryset.filter(tenant=tenant)
            return queryset

        def save_model(self, request, obj, form, change):
            tenant = tenant_from_request(request)
            obj.tenant = tenant
            super().save_model(request, obj, form, change)

With these changes, you have a basic multi-tenant app. But there is a lot more to do as we will see in the following chapters.

The code for this chapter is available at https://github.com/agiliq/building-multi-tenant-applications-with-django/tree/master/shared-db
