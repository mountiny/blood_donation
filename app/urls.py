from django.urls import path, re_path
from django.conf.urls import url
from app import views
import re

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.app, name='app'),
    re_path(r'^app/cancel_booking/$', views.cancel_booking, name='cancel_booking'),
    re_path(r'^app/story/$', views.story, name='story'),
    re_path(r'^app/review/$', views.review, name='review'),
    path('app/write_review/', views.write_review, name='write_review'),
    path('app/map/', views.hospital_map, name='map'),
    path('app/map/all_hospitals/', views.all_hospitals, name='all_hospitals'),
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