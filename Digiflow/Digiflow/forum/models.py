from django.db import models

from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.text import slugify


class Profiles(models.Model):

    user = models.ForeignKey(User,on_delete=models.SET_NULL, related_name="profileUser", null=True )
    points = models.IntegerField(blank=True, null=True)
    bio = models.CharField(max_length=15000)
    first_name = models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    image = models.ImageField(upload_to='static/images/article', blank=True, null=True)

    def __str__(self):
        return str(self.user) or ""


class Answer(models.Model):
    profile=models.ForeignKey(Profiles, on_delete=models.SET_NULL, related_name="profileAnswer", null=True)
    created_at=models.IntegerField(blank=True, null=True)
    body=models.CharField(max_length=15000)
    total_votes=models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.body) or ""



class Question(models.Model):
    profile=models.ForeignKey(Profiles, on_delete=models.SET_NULL, related_name="profileQuestion", null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150,null=True)
    body=models.CharField(max_length=15000)
    total_votes=models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.title) or ""




class Friendship(models.Model):

    friend_one_id = models.ForeignKey(Profiles, on_delete=models.SET_NULL, related_name="Friendship", null=True)
    friend_two_id = models.ForeignKey(Profiles, on_delete=models.SET_NULL, related_name="Friendship2", null=True)

class Vote(models.Model):

    create_at = models.DateTimeField(auto_now_add=True)
    #emiter_profile = models.ForeignKey(Profiles, on_delete=models.SET_NULL, related_name="emiter_profile", null=True)
    #recever_profile = models.ForeignKey(Profiles, on_delete=models.SET_NULL, related_name="recever_profile", null=True)
    type = models.IntegerField(blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, related_name="VoteQuestion", null=True)
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, related_name="VoteAnswer", null=True)



class Tag(models.Model):
    name = models.CharField(max_length=150)
    #id = models.IntegerField

class QuestionsTags(models.Model):
    question_id=models.ForeignKey(Question, on_delete=models.SET_NULL, related_name="TagQuestion", null=True)
    tag_id=models.ForeignKey(Tag, on_delete=models.SET_NULL, related_name="Tag", null=True)


