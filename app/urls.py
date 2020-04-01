from django.urls import path, re_path
from django.conf.urls import url
from app import views
import re

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.app, name='app'),
    re_path(r'^app/story/$', views.story, name='story'),
    path('app/map/', views.hospital_map, name='map'),
    path('app/profile/', views.profile, name='profile'),
    path('app/profile/edit/', views.profile_edit, name='profile_edit'),
    path('app/hospital/<slug:hospital_slug>/',
         views.hospital, name='hospital'),
    path('login/', views.login, name='login'),
    path('app/logout/', views.user_logout, name='logout'),
    re_path(r'^signup/$', views.signup, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('site-map/', views.sitemap, name='sitemap'),
]