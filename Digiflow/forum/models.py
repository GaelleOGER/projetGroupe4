from datetime import date

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    point = models.PositiveIntegerField(default=10)
    bio = models.CharField(max_length=2000)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    following = models.ManyToManyField(User, related_name="following")
    follower = models.ManyToManyField(User, related_name="follower")
    waitinglist = models.ManyToManyField(User, related_name="waitinglist")
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return str(self.user) or ""

    def get_absolute_url(self):
        return reverse('forum:user-profile', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.slug:
            super(Profile, self).save(*args, **kwargs)
        else:
            self.slug = slugify(str(self.user) + str(get_random_string(9)))
            super(Profile, self).save(*args, **kwargs)


class Friend(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friendlist")
    friend = models.OneToOneField(User, on_delete=models.CASCADE, related_name="friend")
    is_accepted = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return str(self.friend) or ""

    # def get_absolute_url(self):
    #     return Profile('account:friend-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.slug:
            super(Friend, self).save(*args, **kwargs)
        else:
            self.slug = slugify(str(self.friend) + get_random_string(9))
            super(Friend, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return str(self.name) or ""

    def save(self, *args, **kwargs):
        if self.slug and self.name.isupper():
            self.name =self.name.upper()
            super(Tag, self).save(*args, **kwargs)
        else:
            self.name = self.name.upper()
            self.slug = slugify(self.name)
            super(Tag, self).save(*args, **kwargs)


class Question(models.Model):
    tags = models.ForeignKey(Tag, blank=True, on_delete=models.CASCADE, null=True, related_name='tagsquestion')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="userquestion")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=500)

    def __str__(self):
        return str(self.title) or ""

    def get_absolute_url(self):
        return reverse('forum:questiondetail',
                       kwargs={'pk': self.pk})


class Vote_Question(models.Model):
    question = models.OneToOneField(Question, on_delete=models.SET_NULL, null=True, related_name="questionvote")
    profile = models.ManyToManyField(User, related_name="userquestionvote", null=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name="questionanswer")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="useranswer")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    body = models.CharField(max_length=550)

    def __str__(self):
        return str(self.pk) or ""

    def get_absolute_url(self):
        return reverse('forum:answer-detail', kwargs={'id': self.pk})


class Vote_Answer(models.Model):
    answer = models.OneToOneField(Answer, on_delete=models.SET_NULL, null=True, related_name="answervote")
    profile = models.ManyToManyField(User, related_name="useranswervote")

