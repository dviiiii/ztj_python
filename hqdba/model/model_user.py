import datetime
from django.db import models
from django.utils import timezone

class User( models.Model ):
    username = models.CharField( max_length=255 )
    userpw = models.CharField( max_length=255 )
    ts = models.DateTimeField('date published')

    def __str__(self):
        return self.username