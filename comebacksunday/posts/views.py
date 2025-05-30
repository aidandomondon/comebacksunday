from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import User, Post

def following(request, user_id) -> HttpResponse:
    """
    Serves the username of every user the specified user follows.
    """
    user = get_object_or_404(User, pk=user_id)
    return render(
        request, 
        'posts/following.html', 
        context={ 'following': user.following }
    )

def user_overview(request, user_id) -> HttpResponse:
    """
    Serves important information about the specified user
    and all posts they have made.
    """
    user = get_object_or_404(User, pk=user_id)
    return render(
        request,
        'posts/user_overview.html',
        context={ 'user': user }
    )

# Will return all posts ever made by every user the specified
# user follows. LIKELY INEFFICIENT, REQUESTS SHOULD BE PAGINATED/CHUNKED
def feed(request, user_id) -> HttpResponse:
    """
    Serves posts from the users the specified user follows.
    """
    user = get_object_or_404(User, pk=user_id)
    # Get all posts in this user's following list, put in reverse chronological order
    posts = Post.objects.filter(author__in=user.following).order_by('-datetime')
    return render(
        request,
        'posts/feed.html',
        context={ 'posts': posts } 
    )
