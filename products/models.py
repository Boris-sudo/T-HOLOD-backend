from django.db import models
from django.contrib.auth.models import User

from fridges.models import Fridge

class Product(models.Model):
    name = models.CharField(max_length=256, null=True, blank=False)
    fridge = models.ForeignKey(to=Fridge, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    count = models.PositiveIntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True,  blank=True)
