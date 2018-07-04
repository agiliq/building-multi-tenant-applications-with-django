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

For the rest of the chapter, we will be using Postgres.

A middleware to set schemas
++++++++++++++++++++++++++++


What about migration?
++++++++++++++++++++++++++++


Beyond the request-response cycle
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
