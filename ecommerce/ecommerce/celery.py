from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установить настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Создание экземпляра Celery
app = Celery('myproject')

# Загрузить настройки из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически искать задачи в приложениях
app.autodiscover_tasks()
