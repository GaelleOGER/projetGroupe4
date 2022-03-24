from django.db import models


# Create your models here.
class User(models.Model):
    id = models.IntegerField


class Profile(models.Model):
    id = models.IntegerField
    user = models.IntegerField
    points = models.IntegerField
    bio = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)


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
