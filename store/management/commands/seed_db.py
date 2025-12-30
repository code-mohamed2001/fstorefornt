from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Populating the database...')

        # 1. Get the path to your SQL file
        current_dir = Path(__file__).parent
        # Ensure this filename is correct
        file_path = os.path.join(current_dir, 'seed.sql')

        with open(file_path, 'r') as f:
            full_sql = f.read()

        # 2. Split the SQL into individual commands
        # We split by semicolon, then strip whitespace
        statements = full_sql.split(';')

        with connection.cursor() as cursor:
            for statement in statements:
                clean_sql = statement.strip()
                if clean_sql:
                    try:
                        cursor.execute(clean_sql)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'Failed on: {clean_sql[:50]}...'))
                        raise e

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
