from django.urls import path
from .views import (
    QuestionDetailView,
    AnswerSubmit,
    ChangeVoteReponse,
    ChangeVoteAnswer,
    home

)

app_name = 'forum'

urlpatterns = [

    path('question/<int:pk>/', QuestionDetailView.as_view(), name='questiondetail'),
    path('answer-create/<int:id>/', AnswerSubmit, name='answer-create'),
    path('question-vote/<int:pk>/', ChangeVoteReponse, name="question-vote"),
    path('answer-vote/<int:pk>/', ChangeVoteAnswer, name="answer-vote"),
    path('', home, name="home"),


]