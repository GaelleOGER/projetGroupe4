from django.urls import path

# il faut importer les views
from .views import *

app_name = 'forum'


urlpatterns = [

    path('createprofile', ProfiCreatetView.as_view(), name="create-profile"),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name="user-profile"),
    path('profile/<int:pk>/update', ProfileUpdateView.as_view(), name="user-profileupdate"),
    path('profileList', ProfileListView.as_view(), name="ajouter-amie"),
    path('Addfriend/<int:pk>/', AddAmie, name="add-friend"),


    ]

