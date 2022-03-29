from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profiles

def user_receiver(sender, instance, created, *args, **kwargs):

    if created:
        Profiles.objects.create(user=instance)


post_save.connect(user_receiver, sender=User)


