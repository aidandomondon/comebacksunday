from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path("create_user", views.create_user, name='create_user'),
    # path("create_post", views.create_post, name='create_post'),
    path("post/<int:post_id>", views.post),
    path("user/<str:username>/profile", views.user_overview, name='profile'),
    path("user/<str:username>/feed", views.feed, name='feed'),
    path("user/<str:username>/following", views.following, name='following')
]
