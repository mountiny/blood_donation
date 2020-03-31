from django.urls import path
from django.conf.urls import url
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.app, name='app'),
    path('app/map/', views.hospital_map, name='map'),
    path('app/profile/', views.profile, name='profile'),
    path('app/profile/edit/', views.profile_edit, name='profile_edit'),
    path('app/hospital/<slug:hospital_slug>/',
         views.hospital, name='hospital'),
    path('login/', views.login, name='login'),
    path('app/logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('site-map/', views.sitemap, name='sitemap'),
]