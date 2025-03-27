# mysite/celery.py
import os
from celery import Celery

# 設定 Django 設定檔的模組路徑（確保是 mysite.settings）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# 建立 Celery app（這個變數名稱必須是 app）
app = Celery('mysite')

# 從 Django 設定中讀取 Celery 設定（以 CELERY_ 為開頭的變數）
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自動尋找各個 app 中的 tasks.py
app.autodiscover_tasks()
