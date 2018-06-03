Shared database with shared schema
---------------------------------------

In this chapter, we will rebuild a sligthly modified Django polls app to be multi-tenant.
You can download the `code from github <https://github.com/agiliq/building-multi-tenant-applications-with-django>`_.

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

Adding multi tenancy
++++++++++++++++++++++++++++

We will add another app called :code:`tenants`

.. code-block:: bash

    python manage.py startapp tenants
