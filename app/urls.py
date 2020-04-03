from django.urls import path, re_path
from django.conf.urls import url
from app import views
import re

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.app, name='app'),
    path('app/notify_donors/', views.notify_donors, name='notify_donors'),
    path('app/write_review/', views.write_review, name='write_review'),
    path('app/write_story/', views.write_story, name='write_story'),
    path('app/book_appointment/', views.book_appointment, name='book_appointment'),
    path('app/map/', views.hospital_map, name='map'),
    path('app/map/all_hospitals/', views.all_hospitals, name='all_hospitals'),
    path('app/profile/', views.profile, name='profile'),
    path('app/profile/edit/', views.profile_edit, name='profile_edit'),
    path('app/hospital/<slug:hospital_slug>/',
         views.hospital, name='hospital'),
    path('app/logout/', views.user_logout, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('site-map/', views.sitemap, name='sitemap'),
    path('login/', views.login, name='login'),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^app/cancel_booking/$', views.cancel_booking, name='cancel_booking'),
    re_path(r'^app/like_story/$', views.like_story, name='like_story'),
    re_path(r'^app/story/$', views.story, name='story'),
    re_path(r'^app/review/$', views.review, name='review'),
    re_path(r'^app/get_new_reviews/$', views.get_new_reviews, name='get_new_reviews'),
    re_path(r'^app/get_new_stories/$', views.get_new_stories, name='get_new_stories'),
]