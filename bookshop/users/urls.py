from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('',include('django.contrib.auth.urls')),
    path('profileauthor/<slug:slug>', views.ProfileView.as_view(), name='profile_author'),
    path('profile/', views.profile, name='profile'),
    path('delete_avatar/', views.delete_avatar, name='delete_avatar'),
    path('profileauthor/<slug:slug>/about/', views.ProfileViewAbout.as_view(), name='profile_about'),

]

    
