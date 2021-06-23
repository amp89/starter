from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
import time
import datetime
from django.shortcuts import reverse
import uuid
from urllib.parse import urljoin
from django.conf import settings

class ActivationCode(models.Model):
    '''
    Created in the Admin Panel
    '''
    expiration_timestamp = models.PositiveIntegerField(default=0)
    code = models.CharField(max_length=100, unique=True)
    one_time_use = models.BooleanField(default=True)

    def save(self, *args, **kwargs):

        if not self.code:
            self.code = str(uuid.uuid4()).upper().replace("-","")

        super(__class__,self).save(*args, **kwargs)

    def check_validity(self):
        if time.time() > self.expiration_timestamp:
            return False
        else:
            return True

    def force_invalidate(self):
        self.expiration_timestamp = 0
        self.save()

    def get_link(self):
        base = reverse("ui:sign_up", kwargs={"code":self.code})
        url = urljoin(settings.SITE_URL, base.lstrip("/"))
        return url
        
    def get_exp_str(self):
        dt = datetime.datetime.fromtimestamp(self.expiration_timestamp)
        if not self.one_time_use:
            return f"{dt.month}/{dt.day}/{dt.year} {dt.hour}:{dt.minute}"
        else:
            return f"{dt.month}/{dt.day}/{dt.year} {dt.hour}:{dt.minute} ONE TIME USE ONLY"



    def __str__(self):
        if not self.one_time_use:
            return f"{self.code} Expires: {self.get_exp_str()}; Link: {self.get_link()}"
        else:
            return f"{self.code} Expires: {self.get_exp_str()}; Link: {self.get_link()}, ONE TIME USE"
