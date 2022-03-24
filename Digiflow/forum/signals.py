from django.contrib.auth.models import User
from django.db.models.signals import post_save

from Digiflow.forum.models import Profile


def user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("Profile créé via signal!")


post_save.connect(user_receiver, sender=User)