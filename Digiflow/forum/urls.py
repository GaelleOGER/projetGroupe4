from django.urls import path

from .views import UserRegistrationView

app_name = 'forum'
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="user-register"),
]