from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.

class userSetting(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, default='KES - Kenyan Shilling')

    def __str__(self):
        return str(self.user)+ ' '+ 'Settings'

def create_user_settings(sender, instance, created, **kwargs):
    
    if created:

        userSetting.objects.create(user=instance)

post_save.connect(create_user_settings, sender=User)