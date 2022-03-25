from django.urls import path

# il faut importer les views
from .views import *

app_name = 'forum'


urlpatterns = [

    path('profile/<int:pk>/', ProfileDetailView.as_view(), name="user-profile"),


    ]

