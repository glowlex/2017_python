from django.core.management.base import BaseCommand, CommandError
from pestyle.models import *
from django.utils.crypto import get_random_string
from random import randint
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass
