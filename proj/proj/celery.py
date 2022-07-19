import os

from celery import Celery, shared_task

from proj.secrects import *

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj',broker='amqp://'+BROKER_USER + ':' + BROKER_PASSWORD + '@localhost//')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
import datetime
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@shared_task(name = "check_notifications_task")
def check_notifications_task(*args, **kwargs):
    print('check_notifications_task')
    from core.tasks import send_telegram_notification
    from core.models import RegisteredUser

    # get all the registerd users
    users = RegisteredUser.objects.all()
    LAST_MESSAGE_MARGIN = datetime.timedelta(minutes=5)
    for user in users:
        # if we are in a 10 secounds window of the prefered time and the last message was sent more than LAST_MESSAGE_MARGIN secounds ago
        if user.preferedNotificationTime - datetime.timedelta(seconds=10) <= datetime.datetime.now().time() <= user.preferedNotificationTime + datetime.timedelta(seconds=10) and user.lastMessageFromUserAt + LAST_MESSAGE_MARGIN < datetime.datetime.now():
            send_telegram_notification(user.id)
    
    # append timestamp to the file 'text.txt'
    with open('text.txt', 'w') as f:
        f.write(str(datetime.datetime.now()) + '\n')
        
    
app.conf.beat_schedule = {
    #Scheduler Name
    'check-notifications-ten-seconds': {
        # Task Name (Name Specified in Decorator)
        'task': 'check_notifications_task',  
        # Schedule      
        'schedule': 10.0,
    },
}