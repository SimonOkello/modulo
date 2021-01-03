from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    notes = models.TextField()
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name



class Expense(models.Model):
    category = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.FloatField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(default=now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.category
