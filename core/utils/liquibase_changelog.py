# utils/liquibase_changelog.py

import datetime
from functools import wraps
import json
import random
import threading
from django.conf import settings

CHANGELOG_FILE = getattr(settings, 'LIQUIBASE_CHANGELOG_PATH', 'liquibase/changelog/master.sql')
CHANGELOG_AUTHOR = getattr(settings, 'LIQUIBASE_CHANGELOG_AUTHOR', 'frontend')

file_lock = threading.Lock()

class LiquibaseChangelogMixin:
    """
    Mixin to auto-append Liquibase changeset to master.sql on create/update.
    """

    def append_liquibase_changeset(self, operation, instance, changed_fields=None):
        print(f"Appending changelog: {operation}, {instance}, {changed_fields}")
        timestamp = int(datetime.datetime.utcnow().timestamp())
        random_id = random.randint(1000, 9999)
        changeset_id = f"{timestamp}-{random_id}"
        table = instance._meta.db_table.replace('"', '')  # Remove any extra quotes

        if operation == 'insert':
            fields = [f.name for f in instance._meta.fields]
            cols = ', '.join(fields)
            vals = ', '.join([self._format_val(getattr(instance, f)) for f in fields])
            sql = f'INSERT INTO {table} ({cols}) VALUES ({vals});'
        elif operation == 'update':
            if not changed_fields:
                return
            set_clause = ', '.join([f"{f}={self._format_val(getattr(instance, f))}" for f in changed_fields])
            # Assumes 'id' is the primary key; adjust as needed
            pk_field = instance._meta.pk.name
            pk_value = getattr(instance, pk_field)
            sql = f'UPDATE {table} SET {set_clause} WHERE {pk_field}={self._format_val(pk_value)};'
        else:
            raise ValueError("Unsupported operation")

        changeset = f"\n--changeset {CHANGELOG_AUTHOR}:{changeset_id}\n{sql}\n"

        with file_lock, open(CHANGELOG_FILE, 'a') as f:
            f.write(changeset)

    def _format_val(self, val):
        if val is None:
            return 'NULL'
        if isinstance(val, str):
            safe_val = val.replace("'", "''")
            return f"'{safe_val}'"
        if isinstance(val, bool):
            return 'TRUE' if val else 'FALSE'
        if isinstance(val, (list, dict)):
            # Store as JSON string for JSONField or text for array
            return f"'{json.dumps(val)}'"
        return str(val)

def liquibase_changelog(operation):
    """
    Decorator to auto-append Liquibase changeset after view logic.
    Usage: @liquibase_changelog('insert') or @liquibase_changelog('update')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            instance = getattr(request, 'liquibase_instance', None)
            changed_fields = getattr(request, 'liquibase_changed_fields', None)
            if instance:
                mixin = LiquibaseChangelogMixin()
                mixin.append_liquibase_changeset(operation, instance, changed_fields)
            return response
        return _wrapped_view
    return decorator