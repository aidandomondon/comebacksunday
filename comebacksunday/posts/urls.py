from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("post/<int:post_id>", views.post),
    path("user/<str:username>/profile", views.user_overview, name='profile'),
    path("user/<str:username>/feed", views.feed, name='feed'),
    path("user/<str:username>/following", views.following, name='following')
]