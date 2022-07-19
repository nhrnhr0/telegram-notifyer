



from django.core.management.base import BaseCommand

from utils.telegramController import tc

class Command(BaseCommand):
    def handle(self, *args, **options):
        tc.start_bot()