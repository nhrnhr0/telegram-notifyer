from django.db import models
import datetime

# Create your models here.
class RegisteredUser(models.Model):
    name = models.CharField(max_length=100)
    telegramId = models.CharField(unique=True, max_length=100)
    lastMessageFromUserAt = models.DateTimeField(null=True)
    LastNotifiedAt = models.DateTimeField(null=True)
    preferedNotificationTime = models.TimeField(null=True)
    def __str__(self):
        return self.name


class UnregisteredUser(models.Model):

    username = models.CharField(max_length=100)
    telegramId = models.CharField(unique=True, max_length=100)
    def __str__(self):
        return self.username + '(' + self.telegramId + ')'
    def register(self):
        from core.tasks import send_telegram_notification
        time_2pm = datetime.time(14, 0)
        user, _ = RegisteredUser.objects.get_or_create(telegramId=self.telegramId, defaults={'name': self.username,
                                                                                            'preferedNotificationTime': time_2pm})
        eta = datetime.datetime.combine(datetime.date.today(), time_2pm)
        if eta < datetime.datetime.now():
            eta = eta + datetime.timedelta(days=1)
        send_telegram_notification.apply_async(args=[user.id], eta=eta)
        user.save()
        self.delete()
        return user
    
