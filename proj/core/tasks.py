

from celery import shared_task
from .models import RegisteredUser
import datetime
from utils.telegramController import tc


@shared_task
def send_telegram_notification(user_id):
    user = RegisteredUser.objects.get(id=user_id)
    user.lastMessageFromUserAt = datetime.datetime.now()
    user.save()
    print('Sending notification to ' + user.name)
    tc.send_message(user.telegramId, 'Hello ' + user.name + '!')
    return True
