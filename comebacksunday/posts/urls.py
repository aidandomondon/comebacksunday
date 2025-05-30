from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("<int:user_id>/profile", views.user_overview, name='profile'),
    path("<int:user_id>/feed", views.following, name='feed'),
    path("<int:user_id>/following", views.following, name='following')
]