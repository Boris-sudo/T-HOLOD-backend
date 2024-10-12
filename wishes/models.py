from django.db import models

from fridges.models import Fridge


class Wishes(models.Model):
    title = models.CharField(max_length=256)
    count = models.IntegerField()
    fridge = models.ForeignKey(to=Fridge, on_delete=models.CASCADE)
