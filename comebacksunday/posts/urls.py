from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path("user_does_not_exist", views.user_does_not_exist, name='user_does_not_exist'),
    path("is_sunday", views.is_sunday, name='is_sunday'),
    path("create_user", views.create_user, name='create_user'),
    path("create_post", views.create_post, name='create_post'),
    path("post/<int:post_id>", views.post),
    path("profile/<str:username>", views.user_overview, name='profile'),
    path("feed", views.feed, name='feed'),
    path("following", views.following, name='following'),
    path("follow", views.follow, name='follow'),
    path("unfollow", views.unfollow, name='unfollow')
]
