from django.core.management.base import BaseCommand, CommandError
import requests
from activation_code_api.models import ActivationCode
import json
import time
from django.contrib.auth.models import User
import datetime


class Command(BaseCommand):
    help = 'CLI To Make a New Activation Code'

    def add_arguments(self, parser):
       parser.add_argument('--hours', type=int, help='Int - How many hours')
       parser.add_argument("--one_time", action='store_true', default=False, help="Flag - One use only?")
       

    def handle(self, *args, **options):
        live_hours = options['hours']
        one_time = options['one_time']
        
        assert isinstance(live_hours, int)
        
        expiration_timestamp = int(time.time()) + int(live_hours*60*60)
        

        activaton_code = ActivationCode.objects.create(
                expiration_timestamp=expiration_timestamp, one_time_use=one_time
            )
        
        print(f"Created: {activaton_code}")