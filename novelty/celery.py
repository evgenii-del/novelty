import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novelty.settings')

app = Celery('novelty')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'change': {
        'task': 'blog.tasks.change_cours',
        'schedule': crontab(minute="*/2"), # Выполнять еждневно в полночь.
    }
}
