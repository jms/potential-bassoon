from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ShortURL(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    submitter = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
