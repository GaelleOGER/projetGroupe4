from django.contrib import admin

# Register your models here.
from .models import Question, Answer, Vote_Question,Vote_Answer
from import_export.admin import ImportExportModelAdmin


class QuestionAdmin(ImportExportModelAdmin):
    list_display = ['user', 'title', 'body']


class AnswerAdmin(ImportExportModelAdmin):
    list_display = ['user', 'body']


class Vote_Question_Admin(ImportExportModelAdmin):
    list_display = ['id', 'question']

class Vote_Answer_Admin(ImportExportModelAdmin):
    list_display = ['id', 'answer']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Vote_Question, Vote_Question_Admin)
admin.site.register(Vote_Answer, Vote_Answer_Admin)

