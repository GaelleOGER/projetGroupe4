from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


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

class Tag(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug and self.name.isupper():
            self.name =self.name.upper()
            super(Tag, self).save(*args, **kwargs)
        else:
            self.name = self.name.upper()
            self.slug = slugify(self.name)
            super(Tag, self).save(*args, **kwargs)





class Question(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=150)
    total_votes = models.IntegerField
    tags = models.ManyToManyField(Tag)




class QuestionsTags(models.Model):
    question_id = models.IntegerField
    tag_id = models.IntegerField



