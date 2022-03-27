from django.urls import path
from .views import (
    QuestionDetailView,
    AnswerSubmit,
    VoteQuestionSetter,
    VoteAnswerSetter, home

)

app_name = 'forum'

urlpatterns = [

    path('question/<int:pk>/', QuestionDetailView.as_view(), name='questiondetail'),
    path('answer-create/<int:id>/', AnswerSubmit, name='answer-create'),
    path('question-vote/<int:pk>/', VoteQuestionSetter, name="question-vote"),
    path('answer-vote/<int:id>/', VoteAnswerSetter, name="answer-vote"),
    path('', home, name="home"),


]