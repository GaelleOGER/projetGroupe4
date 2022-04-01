from django.urls import path, include
from rest_framework import routers

from .views import (
    TokenObtainPairView,
    QuestionApiView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework import routers
router = routers.DefaultRouter()


app_name = 'api'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('question_list', QuestionApiView.as_view(), name='question_list'),

]

from rest_framework.authtoken import views
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]