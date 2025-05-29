# utils/liquibase_changelog.py
import time
import re
import datetime,os
from functools import wraps
import json
import random
import threading
from django.conf import settings

CHANGELOG_MASTER = os.path.join(settings.BASE_DIR, 'liquibase/changelog/master.sql')
CHANGELOG_DIR = os.path.join(settings.BASE_DIR, 'liquibase/changelog/changelogfiles')

# CHANGELOG_AUTHOR = getattr(settings, 'LIQUIBASE_CHANGELOG_AUTHOR', 'frontend')
# CHANGELOG_DIR = getattr(settings, 'LIQUIBASE_CHANGELOG_DIR', 'liquibase/changelog/')

file_lock = threading.Lock()
def get_next_global_master_counter(master_path, username, epoch_ms):
    last_n = 0
    if not os.path.exists(master_path):
        return 1
    with open(master_path, 'r') as f:
        for line in f:
            match = re.match(rf"--changeset {re.escape(username)}:{epoch_ms}-(\d+)", line)
            if match:
                n = int(match.group(1))
                if n > last_n:
                    last_n = n
    return last_n + 1



def get_next_user_master_counter(user_master_path, username):
    last_n = 0
    if not os.path.exists(user_master_path):
        return 1
    with open(user_master_path, 'r') as f:
        for line in f:
            # Match lines like: --changeset username:epoch-counter
            match = re.match(rf"--changeset {re.escape(username)}:\d+-(\d+)", line)
            if match:
                n = int(match.group(1))
                if n > last_n:
                    last_n = n
    return last_n + 1

class LiquibaseChangelogMixin:
    """
    Mixin to auto-append Liquibase changeset to master.sql on create/update.
    """

    import time
    import os

    def append_liquibase_changeset(self, operation, instance, changed_fields=None, username=None, request=None,sessionid=None):
        """
        Appends a changeset to a session-based dummy changelog file, with per-action counter.
        The filename and counter are stored in the session.
        """
        # 1. Get or create session changelog file info
        if request is not None:
            if 'changelog_epoch' not in request.session:
                # First action in this session: create dummy file
                epoch_ms = int(time.time() * 1000)
                dummy_filename = f"{username}-{epoch_ms}.sql"
                request.session['changelog_epoch'] = epoch_ms
                request.session['changelog_counter'] = 1
                request.session['changelog_filename'] = dummy_filename
            else:
                epoch_ms = request.session['changelog_epoch']
                dummy_filename = request.session['changelog_filename']

            counter = request.session['changelog_counter']
        else:
            # fallback: always create a new file if request/session not available
            epoch_ms = int(time.time() * 1000)
            dummy_filename = f"{username}-{epoch_ms}.sql"
            counter = 1

        changelog_path = os.path.join(CHANGELOG_DIR, dummy_filename)
        os.makedirs(os.path.dirname(changelog_path), exist_ok=True)
        header = "--liquibase formatted sql\n"

        # 2. Build the SQL
        table = instance._meta.db_table.replace('"', '')
        if operation == 'insert':
            fields = [f.name for f in instance._meta.fields]
            cols = ', '.join(fields)
            vals = ', '.join([self._format_val(getattr(instance, f), f) for f in fields])
            sql = f'INSERT INTO {table} ({cols}) VALUES ({vals});'
        elif operation == 'update':
            if not changed_fields:
                return
            set_clause = ', '.join([f"{f}={self._format_val(getattr(instance, f), f)}" for f in changed_fields])
            pk_field = instance._meta.pk.name
            pk_value = getattr(instance, pk_field)
            sql = f'UPDATE {table} SET {set_clause} WHERE {pk_field}={self._format_val(pk_value)};'
        else:
            raise ValueError("Unsupported operation")

        # 3. Build the changeset line
        perfile_changeset = f"--changeset {username}:{epoch_ms}-{counter}\n{sql}\n"

        # 4. Write to dummy changelog file
        with file_lock:
            file_exists = os.path.exists(changelog_path)
            with open(changelog_path, 'a') as f:
                if not file_exists:
                    f.write(header)
                f.write(perfile_changeset)

        # 6. (Optional) Also write to user-master.sql if you want
        user_master_filename = f"{username}-master.sql"
        user_master_path = os.path.join(CHANGELOG_DIR, user_master_filename)
        user_master_exists = os.path.exists(user_master_path)
        user_master_counter = get_next_user_master_counter(user_master_path, username)
        user_master_changeset = f"--changeset {username}:{epoch_ms}-{user_master_counter}\n{sql}\n"
        with open(user_master_path, 'a') as f:
            if not user_master_exists:
                f.write(header)
            f.write(user_master_changeset)
        # (You can keep your master logic here if required)
        global_master_path = CHANGELOG_MASTER
        global_master_exists = os.path.exists(global_master_path)
        global_master_counter = get_next_global_master_counter(global_master_path, username, epoch_ms)
        global_master_changeset = f"--changeset {username}:{epoch_ms}-{global_master_counter}\n{sql}\n"
        with open(global_master_path, 'a') as f:
            if not global_master_exists:
                f.write(header)
            f.write(global_master_changeset)
        # 8. Increment counter in session    
        if request is not None:
            request.session['changelog_counter'] = counter + 1

        

    def _format_val(self, val, field=None):
        if val is None:
            return 'NULL'
        if isinstance(val, str):
            if val.strip() == '' or val.strip() in ['{}', '[]']:
                return 'NULL'
            safe_val = val.replace("'", "''")
            return f"'{safe_val}'"
        if isinstance(val, bool):
            return 'TRUE' if val else 'FALSE'
        if isinstance(val, list):
            if not val:
                return 'NULL'
            return json.dumps(val)  # <--- NO single quotes!
        if isinstance(val, dict):
            if not val:
                return 'NULL'
            return json.dumps(val)  # <--- NO single quotes!
        if isinstance(val, (datetime.datetime, datetime.date)):
            return f"'{val.isoformat(sep=' ')}'"
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

import re

def get_next_changeset_number(master_path):
    last_n = 44  # Default start if no changesets (so first will be 45)
    if not os.path.exists(master_path):
        return last_n + 1
    with open(master_path, 'r') as f:
        for line in f:
            match = re.match(r"--changeset\s+\w+:\d+-([0-9]+)", line)
            if match:
                n = int(match.group(1))
                if n > last_n:
                    last_n = n
    return last_n + 1