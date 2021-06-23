from django.core.management.base import BaseCommand, CommandError
import requests
from api.models import *
import json
import time
from django.contrib.auth.models import User
import datetime


class Command(BaseCommand):
    help = 'CLI To Make Activation Code'

    def add_arguments(self, parser):
       parser.add_argument('--hours', type=int, help='How many hours')
       parser.add_argument("--one_time", action='store_true', default=False, help="One use only?")
       

    def handle(self, *args, **options):
        live_hours = options['hours']
        one_time = options['one_time']
        assert isinstance(live_hours, int)
        print(live_hours)
        expiration_timestamp = int(time.time()) + int(live_hours*60*60)
        print(time.time()-expiration_timestamp)

        activaton_code = ActivationCode.objects.create(
                expiration_timestamp=expiration_timestamp, one_time_use=one_time
            )
        

        print(f"Created: {activaton_code}")