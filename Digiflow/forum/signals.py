from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, Question, Vote_Question, Answer, Vote_Answer

def user_receiver(sender, instance, created, *args, **kwargs):

    if created:
        Profile.objects.create(user=instance)


post_save.connect(user_receiver, sender=User)


def vote_question_receiver(sender, instance, created, *args, **kwargs):

    if created:
        Vote_Question.objects.create(question=instance)


post_save.connect(vote_question_receiver, sender=Question)


def vote_answer_receiver(sender, instance, created, *args, **kwargs):

    if created:
        Vote_Answer.objects.create(answer=instance)


post_save.connect(vote_answer_receiver, sender=Answer)


