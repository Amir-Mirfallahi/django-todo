from celery import shared_task
from .models import Task

@shared_task
def remove_tasks():
    Task.objects.filter(status=True).delete()
