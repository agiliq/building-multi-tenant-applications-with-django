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
