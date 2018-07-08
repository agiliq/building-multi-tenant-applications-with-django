Third party apps
-------------------

Open source Django multi tenancy apps
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


There are number of third party Django apps which add multi tenancy to Django.

Some of them are

- Django multitenant: https://github.com/citusdata/django-multitenant (Shared SChema, Shared DB, Tables have :code:`tenant_id`)
- Django tenant schemas: https://github.com/bernardopires/django-tenant-schemas (Isolated Schemas, shared DB)
- Django db multitenant: https://github.com/mik3y/django-db-multitenant (Isolated DB)

We will look in detail at Django tenant schemas, which is our opinion is the most mature of the Django multi tenancy solutions.

A tour of django-tenant-schemas
++++++++++++++++++++++++++++++++++


Install :code:`django-tenant-schemas` using pip. :code:`pip install django-tenant-schemas`. Verify the version of django-tenant-schemas that got installed.

.. code-block:: bash

    $ pip freeze | grep django-tenant-schemas
    django-tenant-schemas==1.9.0


We will start from our non tenant aware Polls app and add multi tenancy using django-tenant-schemas.

Create a new database, and make sure your Django app picks up the new DB by updating the :code:`DATABASE_URL` environment var.

Update your settings to use the tenant-schemas :code:`DATABASE_BACKEND` and tenant-schemas :code:`DATABASE_ROUTERS`


.. code-block:: python

    DATABASES["default"]["ENGINE"] = "tenant_schemas.postgresql_backend"
    # ...
    DATABASE_ROUTERS = ("tenant_schemas.routers.TenantSyncRouter",)

The :code:`postgresql_backend` will ensure that the connection has the correct :code:`tenant` set, and the :code:`TenantSyncRouter`
will ensure that the migrations run correctly.

Then create a new app called :code:`tenants` with :code:`manage.py startapp`, and create a new :code:`Client` model

.. code-block:: python

    from tenant_schemas.models import TenantMixin


    class Client(TenantMixin):
        name = models.CharField(max_length=100)

In your settings, change the middleware and set the :code:`TENANT_MODEL`.

.. code-block:: python

    TENANT_MODEL = "tenants.Client"
    # ...

    MIDDLEWARE = [
        "tenant_schemas.middleware.TenantMiddleware",
        # ...
        ]

:code:`tenant-schemas` comes with the concept of :code:`SHARED_APPS` and :code:`TENANT_APPS`.
The apps in :code:`SHARED_APPS` have their tables in public schema, while the apps in :code:`TENANT_APPS` have their tables in tenant specific schemas.


.. code-block:: python

    SHARED_APPS = ["tenant_schemas", "tenants"]

    TENANT_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "rest_framework",
        "rest_framework.authtoken",
        "polls",
    ]

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

We are almost done. We need to

- Run the migrations in the public schema
- Create the tenants and run migrations in all the tenant schemas
- Create a superuser in tenant schemas

:code:`tenant-schemas` has the :code:`migrate_schemas` which replaces the :code:`migrate` command.
It is tenant aware and will sync :code:`SHARED_APPS` to public schema, and :code:`TENANT_APPS` to tenant specific schemas.

Run :code:`python manage.py migrate_schemas --shared` to sync the public tables.

The run a python shell using :code:`python manage.py shell`, and create the two tenants, using

.. code-block:: python

    Client.objects.create(name="thor",
        schema_name="thor", domain_url="thor.polls.local")
    Client.objects.create(name="potter",
        schema_name="potter", domain_url="potter.polls.local")


This will create the schemas in the table and run the migrations. You now need to create the superuser in the tenant schema so that you can access the admin.
The :code:`tenant_command` command allow running any Django command in the context of any tenant.

.. code-block:: bash

    python manage.py tenant_command createsuperuser
    
 And we are done. We can now access the tenant admins, create polls and view the tenant specific API endpoints.
 
The code for this chapter is available at https://github.com/agiliq/building-multi-tenant-applications-with-django/tree/master/tenant-schemas-demo .
