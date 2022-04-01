from django.urls import path
from .views import *


app_name = 'forum'
# forum-question = home



urlpatterns = [

    path('<int:pk>/update/', QuestionUpdateView.as_view(), name="question-update"),
    path('<int:pk>/delete/', QuestionDeleteView.as_view(), name="question-delete"),

    path('add-friend/<int:pk>/', AddFriendRelationship, name='add-friend'),
    path('remove-friend/<int:pk>/', RemoveFriendRelationship, name='remove-friend'),

    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('login/submit/', ConnectAjax, name='login-submit'),
    path('tag/create/', TagCreateView.as_view(), name="tag-create"),
    path('tag/<str:slug>/', TagView.as_view(), name="tag"),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='questiondetail'),
    path('answer-create/<int:id>/', AnswerSubmit, name='answer-create'),
    path('question-create/', QuestionCreateView.as_view(), name='question-create'),
    path('question-vote/<int:pk>/', ChangeVoteQuestion, name="question-vote"),
    path('answer-vote/<int:pk>/', ChangeVoteAnswer, name="answer-vote"),
    path('createprofile', ProfileCreateView.as_view(), name="create-profile"),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name="user-profile"),
    path('profile/<int:pk>/update', ProfileUpdateView.as_view(), name="user-profileupdate"),
    path('profileList', ProfileListView.as_view(), name="ajouter-amie"),

    path('following/<str:slug>', FollowingListOfUser.as_view(), name="following-list"),
    path('follower/<str:slug>', FollowerListOfUser.as_view(), name="follower-list"),

    path('', HomeView.as_view(), name="home"),
    path('list_question', QuestionListView.as_view(), name="forum-question"),
    path('logout', Logout, name="logout"),
    path('search-question', SearchQuestion, name="search-question"),

]

   
    