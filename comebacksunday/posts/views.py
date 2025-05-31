from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import ExtendedUser, Post
from django.forms import Form, EmailField, EmailInput, CharField, PasswordInput, Textarea

def following(request, username) -> HttpResponse:
    """
    Serves the username of every user the specified user follows.
    """
    try:
        extended_user = ExtendedUser.objects.get(user__username=username)
    except ExtendedUser.DoesNotExist:
        raise Http404(f"User {username} does not exist.")
    return render(
        request, 
        'posts/following.html', 
        context={ 'following': extended_user.following.all() }
    )

def user_overview(request, username) -> HttpResponse:
    """
    Serves important information about the specified user
    and all posts they have made.
    """
    try:
        extended_user = ExtendedUser.objects.get(user__username=username)
    except ExtendedUser.DoesNotExist:
        raise Http404(f"User {username} does not exist.")
    return render(
        request,
        'posts/user_overview.html',
        context={ 
            'username': extended_user.user.username,
            'bio': extended_user.bio,
            'posts': extended_user.post_set.all()
        }
    )

# Will return all posts ever made by every user the specified
# user follows. LIKELY INEFFICIENT, REQUESTS SHOULD BE PAGINATED/CHUNKED
def feed(request, username) -> HttpResponse:
    """
    Serves posts from the users the specified user follows.
    """
    try:
        extended_user = ExtendedUser.objects.get(user__username=username)
    except ExtendedUser.DoesNotExist:
        raise Http404(f"User {username} does not exist.")
    # Get all posts in this user's following list, put in reverse chronological order
    posts = Post.objects \
        .filter(author__in=extended_user.following.all()) \
        .order_by('-datetime').all()
    return render(
        request,
        'posts/feed.html',
        context={ 'posts': posts } 
    )

def post(request, post_id) -> HttpResponse:
    """
    Serves information about the post specified by its ID.
    """
    return render(
        request,
        'posts/post.html',
        context={ 'post': get_object_or_404(Post, pk=post_id) }
    )

# We are using a regular Form rather than a ModelForm because we
# need to execute intermediate steps when constructing our ExtendedUser
# (namely, creating the User that the ExtendedUser will have). ModelForms
# are used when the Model can be created _directly_ from the arguments of the form. 
class CreateExtendedUserForm(Form):
    """
    To ingest, store, validate, and clean input data for the form
    that creates `ExtendedUser`s.
    """
    email = EmailField(widget=EmailInput)
    username = CharField(max_length=75)
    password = CharField(max_length=100, widget=PasswordInput)
    bio = CharField(max_length=280, widget=Textarea)


def create_user(request) -> HttpResponse:
    """
    When called with the GET method:
    - Serves the form to create `ExtendedUsers`
    When called with the POST method (and data):
    - takes in the data attempts to use it to create an `ExtendedUsers`
    - if data is not valid, serves the form back up again.
    """
    if request.method == "GET":     # Method is set to "GET" when starting a new form...
        form = CreateExtendedUserForm()
        return render(
            request,
            'posts/create_user.html',
            context={ "form": form }
        )
    elif request.method == "POST":  # ...and "POST" if returning w/ data from a filled out form
        form = CreateExtendedUserForm(data=request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            try:
                user = User.objects.create_user(
                    username = cleaned_data["username"], 
                    email = cleaned_data["email"], 
                    password = cleaned_data["password"],
                )
                ExtendedUser.objects.create(
                    user = user,
                    bio = cleaned_data["bio"],
                )
                return HttpResponse('Success.')
            except IntegrityError as e:
                return HttpResponse(e.__str__())
        else:
            # if not valid, return client the view again 
            # (but still populated with in-progress entries)
            return render(
                request,
                'posts/create_user.html',
                context={ "form": form }
            )
    else:
        return HttpResponseBadRequest(f"Unsupported HTTP method: {request.method}")
