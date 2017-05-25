from celery.task import periodic_task
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from .models import *
from .scripts.gen_looks import Looks

@periodic_task(run_every = timedelta(hours = 8))
def test():
    users = User.objects.all();
    for us in users:
        looks = Look_suggestions.objects.filter(user=us)
        if looks.count()> 15:
            continue
        genl = Looks(us)
        n = genl.generate_looks()
        logger.info(str(us)+' '+str(n))
