from django.db import models
from django.db.models import Model

class empinfo(models.Model):
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=30)
    age = models.IntegerField()