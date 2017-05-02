from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        settings.MEDIA_ROOT = settings.BASE_DIR+'/pestyle/static/test_images'
        call_command('fill', users=1, items=20, looks=20, looks_s=20, events=3, test=True)
