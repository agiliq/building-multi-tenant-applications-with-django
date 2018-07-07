Tying it all together
------------------------

Launching new tenants
++++++++++++++++++++++++++++

In the previous chapters, we have worked with a hardcoded list, of two tenants, :code:`thor` and :code:`potter`. Our code looked like this

code-block:: python

    def get_tenants_map():
        return {"thor.polls.local": "thor", "poter.polls.local": "potter"}

In a real scenario, you will need to launch tenants, so the list of tenants can't be part of the code. To be able to launch new tenants, we will create a :code:`Tenant` model.

code-block:: python

    class Tenant(models.Model):
        name = models.CharField(max_length=100)
        schema_name = models.CharField(max_length=100)
        subdomain = models.CharField(max_length=1000, unique=True)

And your :code:`get_tenants_map` will change to:

code-block:: python

    def get_tenants_map():
        return dict(Tenant.objects.values_list("subdomain", "schema_name"))

You would need to make similar changes for a multi DB setup, or orchestrate launching new containers and updating nginx config for multi container setup.


A comparison of trade-offs of various methods
+++++++++++++++++++++++++++++++++++++++++++++++

Until now, we had looked at four different ways of doing multi tenancy, each with some set of trade-offs.

Depending upon how many tenants you have, how many new tenants you need to launch, and your customization requirements, one of the four architectures will suit you.


=======================     ==========   ==================  ====================================
Method                      Isolation    Time to             Django DB
                                         launch new tenants  Compatibility
=======================     ==========   ==================  ====================================
Shared DB and Schema        Low          Low                 High (Supported in all DBs)
Isolated Schema             Medium       Low                 Medium (DB must support schema)
Isolated DB                 High         Medium              High (Supported in all DBs)
Isolated using docker       Complete     Medium              High (Supported in all DBs)
=======================     ==========   ==================  ====================================



What method should I use?
++++++++++++++++++++++++++++++++++++++++++++

While each method has its pros and cons, for most people, Isolated Schema with shared database is the best method.
It provides strong isolation guarantees, customizability with minimal time to launch new tenants.

