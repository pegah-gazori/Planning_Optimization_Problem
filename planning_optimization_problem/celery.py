"""
* File Name: celery.py
* Django App Name: planning_optimization_problem
* Description:
  This file contains the initializations of the Celery which are mentioned as follows:
  - Setting the default Django settings module for the 'celery' program.
  - Setting the Celery backend and broker.
  - Determining the Celery configuration file.
  - Loading task modules from all registered Django apps.
"""

import os
from celery import Celery
from planning_optimization_problem.settings import (CELERY_BROKER_URL, CELERY_RESULT_BACKEND)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planning_optimization_problem.settings')
app = Celery('planning', backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL)
app.config_from_object("django.conf:settings", namespace='CELERY')
app.autodiscover_tasks()
