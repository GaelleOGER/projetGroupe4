from django.contrib import admin

# Register your models here.
from .models import Question, Answer, Vote_Question, Vote_Answer, Profile, Tag, Friend



class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'body', 'pk']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'body']


class Vote_Question_Admin(admin.ModelAdmin):
    list_display = ['id', 'question']


class Vote_Answer_Admin(admin.ModelAdmin):
    list_display = ['id', 'answer']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'point']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Vote_Question, Vote_Question_Admin)
admin.site.register(Vote_Answer, Vote_Answer_Admin)
admin.site.register(Tag)
admin.site.register(Friend)