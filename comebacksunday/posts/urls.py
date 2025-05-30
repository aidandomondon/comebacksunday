from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("<str:username>/profile", views.user_overview, name='profile'),
    path("<str:username>/feed", views.following, name='feed'),
    path("<str:username>/following", views.following, name='following')
]