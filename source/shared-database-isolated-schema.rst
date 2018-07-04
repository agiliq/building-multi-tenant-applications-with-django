Shared database with isolated schema
---------------------------------------

Limitations of shared schema and our current method
++++++++++++++++++++++++++++++++++++++++++++++++++++++

In the previous chapter we used a :code:`ForeignKey` to separate the tenants. This method is simple
but limited due to the following limitations.

- Weak separation of tenant's data
- Tenant isolation code is intermixed with app code
- Duplication of code


Weak separation of tenant's data
=================================

Because each tenant's data stays in the same schema, there is no way to limit access to a single tenant's data at the DB level.


Tenant isolation code is intermixed with app code
==================================================

You need to litter your code with :code:`.filter(tenant=tenant)` every time you access db. For example in your :code:`ViewSet` you would be doing this:

.. code-block:: python

    def get_queryset(self):
        tenant = tenant_from_request(self.request)
        return super().get_queryset().filter(tenant=tenant)

If you even miss a :code:`filter`, you would be mixing data from two tenants. This will be a bad security bug.


Duplication of code
============================


The tenant separation code of getting the tenant from the request and filtering on it is all over your codebase, rather than a central location.

In this chapter, we will rearchitect our code to use Shared database with isolated schema, which will fix most of these limitations.



What are database schemas?
+++++++++++++++++++++++++++

Schemas in database are a way to group objects. Postgres documentation defines schema as

    A database contains one or more named schemas, which in turn contain tables. Schemas also contain other kinds of named objects, including data types, functions, and operators. The same object name can be used in different schemas without conflict; for example, both schema1 and myschema may contain tables named mytable.

For the rest of the chapter, we will be using Postgres. We will be using one schema per tenant.

We need some way to keeping a mapping on tenants to schemas. There are a number of ways you could do it, for example by keeping a table in public schema to map tenant urls to schemas. In this chapter, for simplicity,  we will keep a simple map of tenant urls to schemas.

Add this to your utils.py

.. code-block:: python

    def get_tenants_map():
        return {
            "thor.polls.local": "thor",
            "potter.polls.local": "potter",
        }

Now when we get a request to :code:`thor.polls.local` we need to read from the schema :code:`thor`, and when we get a request to :code:`potter.polls.local` we need to read from schema :code:`potter`.



Managing database migrations
++++++++++++++++++++++++++++

:code:`manage.py migrate` is not schema aware. So we will need to subclass this command so that tables are created in all the schemas. Create the folder structure for a new command following the usual django convention. Then add a file named :code:`migrate_schemas` in there.


.. code-block:: python

    from django.core.management.commands.migrate import Command as MigrationCommand

    from django.db import connection
    from ...utils import get_tenants_map


    class Command(MigrationCommand):
        def handle(self, *args, **options):
            with connection.cursor() as cursor:
                schemas = get_tenants_map().values()
                for schema in schemas:
                    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
                    cursor.execute(f"SET search_path to {schema}")
                    super(Command, self).handle(*args, **options)


To understand what we are doing here, you need to know a few postgres queries.

- :code:`CREATE SCHEMA IF NOT EXISTS potter` creates a new schema named potter.
- :code:`SET search_path to potter` set the connection to use the given schema.

Now when you run :code:`manage.py migrate_schemas` it loops over the our tenants map, the creates a schema for that tenant, and runs the migration for the tenant.


A middleware to set schemas
++++++++++++++++++++++++++++





Beyond the request-response cycle
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
