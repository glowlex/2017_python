from django.core.management.base import BaseCommand, CommandError
from pestyle.models import *
from django.utils.crypto import get_random_string
from random import randint
from datetime import datetime, timedelta
from pestyle.lists import *
from requests import get
from django.core.files import File


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(options.get('e', 'not argum'))
