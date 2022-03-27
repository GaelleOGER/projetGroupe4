from datetime import date

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.urls import reverse


class Profile(models.Model):
    id = models.IntegerField
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="userprofile")
    points = models.IntegerField
    bio = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)


class Friendship(models.Model):

    friend_one_id = models.IntegerField
    friend_two_id = models.IntegerField


class Tag(models.Model):

    name = models.CharField(max_length=150)


class QuestionsTags(models.Model):
    question_id = models.IntegerField
    tag_id = models.IntegerField


class Question(models.Model):

    tags = models.ManyToManyField(Tag, blank=True, null=True, related_name='tagsquestion')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="userquestion")
    profile = models.IntegerField
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=500)
    total_votes = models.IntegerField(blank=True, null=True, default=0)
    votes_counter = models.PositiveIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.title) or ""

class Answer(models.Model):

    question = models.ForeignKey(Question,on_delete=models.SET_NULL, null=True, related_name="questionanswer")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="useranswer")
    profile = models.IntegerField
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    body = models.CharField(max_length=550)
    total_votes = models.IntegerField(blank=True, null=True, default=0)
    votes_counter = models.PositiveIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.pk) or ""

    def get_absolute_url(self):
        return reverse('forum:answer-detail', kwargs={'id':self.pk})

class Vote(models.Model):

    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name="questionvote")
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, related_name="answervote")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    emitter_profile = models.IntegerField
