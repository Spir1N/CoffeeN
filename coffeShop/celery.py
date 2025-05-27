import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeShop.settings')

app = Celery('coffeShop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
