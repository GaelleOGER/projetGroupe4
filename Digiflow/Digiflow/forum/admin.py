from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profiles)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Friendship)
admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(QuestionsTags)