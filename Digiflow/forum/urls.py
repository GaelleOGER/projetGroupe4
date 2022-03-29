from django.urls import path
from .views import *


app_name = 'forum'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('login/submit/', ConnectAjax, name='login-submit'),
    path('home/', HomeView.as_view(), name="home"),
    path('tag/create/', TagCreateView.as_view(), name="tag-create"),
    path('tag/<str:slug>/', TagView.as_view(), name="tag"),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='questiondetail'),
    path('answer-create/<int:id>/', AnswerSubmit, name='answer-create'),
    path('question-vote/<int:pk>/', ChangeVoteReponse, name="question-vote"),
    path('answer-vote/<int:pk>/', ChangeVoteAnswer, name="answer-vote"),
    path('createprofile', ProfiCreatetView.as_view(), name="create-profile"),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name="user-profile"),
    path('profile/<int:pk>/update', ProfileUpdateView.as_view(), name="user-profileupdate"),
    path('profileList', ProfileListView.as_view(), name="ajouter-amie"),
    path('Addfriend/<int:pk>/', AddAmie, name="add-friend"),
    path('following/<str:slug>', FollowingListOfUser.as_view(), name="following-list"),
    path('follower/<str:slug>', FollowerListOfUser.as_view(), name="follower-list"),
    path('', home, name="home"),
]

   
    