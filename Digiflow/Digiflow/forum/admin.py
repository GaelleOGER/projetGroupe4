from django.contrib import admin
from .models import *

# Register your models here.

class ProfilesAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'points']

admin.site.register(Profiles, ProfilesAdmin)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(QuestionsTags)