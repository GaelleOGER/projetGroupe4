from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Profile, Vote_Question, Question


def user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(user_receiver, sender=User)
