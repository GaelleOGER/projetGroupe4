from django.contrib import admin

# Register your models here.
from .models import Question, Answer
from import_export.admin import ImportExportModelAdmin


class QuestionAdmin(ImportExportModelAdmin):
    list_display = ['user', 'title', 'body', 'total_votes']


class AnswerAdmin(ImportExportModelAdmin):
    list_display = ['user', 'body', 'total_votes']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

