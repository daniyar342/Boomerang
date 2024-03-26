# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config',backend='redis', broker="redis://0.0.0.0:6380/0")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

