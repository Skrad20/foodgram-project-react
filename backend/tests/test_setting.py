
from django.test import TestCase
from django.db import connection
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.foodgram.settings'


class TEST_DB(TestCase):
    'Проверка названия базы данных.'
    def test_db(self):
        db_name = connection.settings_dict['NAME']
        assert db_name == 'postgres', 'неправильная БД'
