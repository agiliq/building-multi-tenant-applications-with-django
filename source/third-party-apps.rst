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
