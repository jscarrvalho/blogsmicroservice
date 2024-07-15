from django.core.management.base import BaseCommand
import MySQLdb
from django.conf import settings


class Command(BaseCommand):
    help = 'Create database if it does not exist'

    def handle(self, *args, **kwargs):
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']

        conn = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_password,
            port=int(db_port)
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        conn.close()
