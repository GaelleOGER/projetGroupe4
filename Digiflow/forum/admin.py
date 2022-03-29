from django.contrib import admin

# Register your models here.
from .models import Tag, Question

admin.site.register(Tag)
admin.site.register(Question)
