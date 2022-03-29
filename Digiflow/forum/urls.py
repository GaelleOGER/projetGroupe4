from django.urls import path

from .views import UserRegistrationView, HomeView, UserLoginView, TagView, TagCreateView, ConnectAjax

app_name = 'forum'
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('login/submit/', ConnectAjax, name='login-submit'),
    path('home/', HomeView.as_view(), name="home"),
    path('tag/create/', TagCreateView.as_view(), name="tag-create"),
    path('tag/<str:slug>/', TagView.as_view(), name="tag"),
]