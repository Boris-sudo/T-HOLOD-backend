from django.db import models
from django.contrib.auth.models import User


class Fridge(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="owner")
    admins = models.ManyToManyField(to=User, related_name="admins")
    members = models.ManyToManyField(to=User, related_name="members")
