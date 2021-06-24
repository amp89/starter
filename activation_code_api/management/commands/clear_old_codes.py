from django.core.management.base import BaseCommand, CommandError
from activation_code_api.models import ActivationCode
import json
import time
from django.contrib.auth.models import User



class Command(BaseCommand):
    help = 'CLI To Delete Old Activation Codes'

    def add_arguments(self, parser):
       parser.add_argument('--confirm', action='store_true', default=False, help='Prevent Accidental Deletes')
       
       

    def handle(self, *args, **options):
        if not options['confirm']:
            raise Exception("You must pass --confirm if you're sure you want to delete all of the old codes")
        
        for code in ActivationCode.objects.all():
            '''
            Less efficient, but allows me to change the check_validity method later
            '''
            if code.check_validity() == False:
                print(f"Deleting: {code}")
                code.delete()
                print(f"Deleted")