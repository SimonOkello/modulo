from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class Source(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Income(models.Model):
    source = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.FloatField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(default=now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.source
