from django.urls import path
from .views import *


app_name = 'forum'

urlpatterns = [

    path('question/<int:pk>/', QuestionDetailView.as_view(), name='questiondetail'),
    path('answer-create/<int:id>/', AnswerSubmit, name='answer-create'),
    path('question-vote/<int:pk>/', ChangeVoteReponse, name="question-vote"),
    path('answer-vote/<int:pk>/', ChangeVoteAnswer, name="answer-vote"),
    path('createprofile', ProfiCreatetView.as_view(), name="create-profile"),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name="user-profile"),
    path('profile/<int:pk>/update', ProfileUpdateView.as_view(), name="user-profileupdate"),
    path('profileList', ProfileListView.as_view(), name="ajouter-amie"),
    path('Addfriend/<int:pk>/', AddAmie, name="add-friend"),
    path('', home, name="home"),


]