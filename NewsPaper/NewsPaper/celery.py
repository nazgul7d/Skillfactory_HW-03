from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
 
app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'weekly_newsletter': {
        'task': 'news.tasks.newsletter',
        'schedule': crontab(hour = 8, minute = 0, day_of_week = 1),
    }
}