from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin, User

from forum.models import Profile

class UserProfileInline(admin.StackedInline):
    model = Profile

class ProfileAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)