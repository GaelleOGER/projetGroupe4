from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    points = models.IntegerField(default=10)
    bio = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, default='User First Name')
    last_name = models.CharField(max_length=150, default='Last Name')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user')


class Friendship(models.Model):

    friend_one_id = models.IntegerField
    friend_two_id = models.IntegerField


class Answer(models.Model):
    id = models.IntegerField
    profile = models.IntegerField
    created_at = models.IntegerField
    body = models.CharField(max_length=150)
    total_votes = models.IntegerField


class Vote(models.Model):
    created_at = models.DateTimeField
    emitter_profile = models.IntegerField
    receiver_profile = models.IntegerField
    type = models.IntegerField
    question = models.IntegerField
    answer = models.IntegerField


class Question(models.Model):
    id = models.IntegerField
    profile = models.IntegerField
    created_at = models.DateTimeField
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=150)
    total_votes = models.IntegerField


class QuestionsTags(models.Model):
    question_id = models.IntegerField
    tag_id = models.IntegerField


class Tag(models.Model):
    id = models.IntegerField
    name = models.CharField(max_length=150)
