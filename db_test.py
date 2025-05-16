import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loanos_project.settings")
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT 1 FROM question_master LIMIT 1;")
    row = cursor.fetchone()
    print("DB Connection Successful! Row:", row)