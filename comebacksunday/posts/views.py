from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import User, Post

def following(request, username) -> HttpResponse:
    """
    Serves the username of every user the specified user follows.
    """
    user = get_object_or_404(User, pk=username)
    return render(
        request, 
        'posts/following.html', 
        context={ 'following': user.following.all() }
    )

def user_overview(request, username) -> HttpResponse:
    """
    Serves important information about the specified user
    and all posts they have made.
    """
    user = get_object_or_404(User, pk=username)
    return render(
        request,
        'posts/user_overview.html',
        context={ 
            'username': user.username,
            'bio': user.bio,
            'posts': user.post_set
        }
    )

# Will return all posts ever made by every user the specified
# user follows. LIKELY INEFFICIENT, REQUESTS SHOULD BE PAGINATED/CHUNKED
def feed(request, username) -> HttpResponse:
    """
    Serves posts from the users the specified user follows.
    """
    user = get_object_or_404(User, pk=username)
    # Get all posts in this user's following list, put in reverse chronological order
    posts = Post.objects.filter(author__in=user.following.all()).order_by('-datetime').all()
    return render(
        request,
        'posts/feed.html',
        context={ 'posts': posts } 
    )
