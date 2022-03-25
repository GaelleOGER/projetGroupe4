from django.urls import path
from .views import (
    QuestionDetailView,
    AnswerSubmit,
)

app_name = 'forum'

urlpatterns = [

    path('question/<int:pk>/', QuestionDetailView.as_view(), name='questiondetail'),
    path('answer-create/<int:id>/', AnswerSubmit, name='answer-create'),


]