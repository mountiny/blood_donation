from django.urls import path
from django.conf.urls import url
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.app, name='app'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]