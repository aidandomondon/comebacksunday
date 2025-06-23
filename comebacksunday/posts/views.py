from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import ExtendedUser, Post
from django.forms import Form, EmailField, EmailInput, CharField, PasswordInput, Textarea
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm
from django.urls import reverse
from datetime import datetime, timezone, timedelta
from enum import Enum
from django.contrib.auth import login

@login_required
def following(request) -> HttpResponse:
    """
    Serves the username of every user the specified user follows.
    """
    username = request.user.username
    extended_user = ExtendedUser.objects.get(user__username=username)
    return render(
        request, 
        'posts/following.html', 
        context={ 'username': username, 'following': extended_user.following.all() }
    )

@login_required
def follow(request) -> HttpResponse:
    """
    Makes the logged-in user follow the user specified in the POST data.
    """
    if request.method == 'POST':
        follower = ExtendedUser.objects.get(user__username=request.user.username)
        followee_username = request.POST["followee_username"]
        followee = ExtendedUser.objects.get(user__username=followee_username)
        follower.following.add(followee)
        return HttpResponseRedirect(reverse('posts:following'))
    else:
        return HttpResponse("Unsupported HTTP method.")
    
def unfollow(request) -> HttpResponse:
    """
    Removes the user specified in the POST data from the logged-in user's following list
    """
    if request.method == 'POST':
        follower = ExtendedUser.objects.get(user__username=request.user.username)
        followee_username = request.POST["followee_username"]
        followee = ExtendedUser.objects.get(user__username=followee_username)
        follower.following.remove(followee)
        return HttpResponseRedirect(reverse('posts:following'))
    else:
        return HttpResponse("Unsupported HTTP method.")

def user_overview(request, username) -> HttpResponse:
    """
    Serves important information about the specified user
    and all posts they have made.
    """
    extended_user = ExtendedUser.objects.get(user__username=username)
    return render(
        request,
        'posts/user_overview.html',
        context={ 
            'username': extended_user.user.username,
            'bio': extended_user.bio,
            'posts': extended_user.post_set.order_by('-datetime').all()
        }
    )

class Countdown:
    def __init__(self, days: int, hours: int, minutes: int):
        self.days = days
        self.hours = hours
        self.minutes = minutes

    def is_zero(self) -> bool:
        return self.days == 0 and self.hours == 0 and self.minutes == 0

def _countdown() -> Countdown:
    # Returns a timedelta representing the amount of time until it is Sunday anywhere on Earth.
    # If it is currently Sunday anywhere on Earth, returns a timedelta of 0.
    if _is_sunday():
        return Countdown(0, 0, 0)
    else:
        kiribati_tz = timezone(offset=timedelta(hours=+14))
        kiribati_now = datetime.now(tz=kiribati_tz)
        # Find how many days until next sunday
        kiritbati_days_until_sunday: int = 7 - kiribati_now.weekday()
        # Add that to the beginning of today to find the beginning of next sunday
        kiribati_beginning_of_today = datetime(
            kiribati_now.year,
            kiribati_now.month, 
            kiribati_now.day, 
            0, 0, 0,
            tzinfo=kiribati_tz
        )
        kiribati_beginning_of_next_sunday: datetime = \
            kiribati_beginning_of_today \
            + timedelta(days=kiritbati_days_until_sunday)
        # Subtract today to find the time until the beginning of next sunday
        timedelta_to_next_sunday: timedelta = kiribati_beginning_of_next_sunday - kiribati_now

        # Extract days, minutes, and seconds from the `timedelta`.
        # str() method of `timedelta` returns 'day(s), h:m:s.ms'
        countdown_days, countdown_hms = str(timedelta_to_next_sunday).split(', ')
        countdown_days = int(countdown_days.replace(' days', '').replace(' day', ''))
        countdown_hours, countdown_minutes, _ = map(int, countdown_hms.split('.')[0].split(':'))
        return Countdown(countdown_days, countdown_hours, countdown_minutes)
    
def _last_sunday() -> datetime:
    # Returns a datetime representing the beginning of the last Sunday in Kiribati.
    # If it is currently Sunday, returns the beginning of today in Kiribati
    kiribati_tz = timezone(offset=timedelta(hours=+14))
    kiribati_now = datetime.now(tz=kiribati_tz)
    kiribati_beginning_of_today: datetime = datetime(
        kiribati_now.year,
        kiribati_now.month, 
        kiribati_now.day, 
        0, 0, 0,
        tzinfo=kiribati_tz
    )
    if _is_sunday():
        return kiribati_beginning_of_today
    else:
        # Find how many days in Kiribati since it was last sunday
        kiritbati_days_since_sunday: int = kiribati_now.weekday()
        return kiribati_beginning_of_today - timedelta(days=kiritbati_days_since_sunday)

# Will return all posts ever made by every user the specified
# user follows. LIKELY INEFFICIENT, REQUESTS SHOULD BE PAGINATED/CHUNKED
@login_required
def feed(request) -> HttpResponse:
    """
    Serves posts from the users the specified user follows.
    """
    username = request.user.username
    extended_user = ExtendedUser.objects.get(user__username=username)
    
    # Get all posts in this user's following list, put in reverse chronological order
    posts = Post.objects \
        .filter(author__in=extended_user.following.all()) \
        .filter(datetime__gte=_last_sunday().strftime("%Y-%m-%d")) \
        .order_by('-datetime').all()
    
    # countdown to next sunday
    countdown: Countdown = _countdown() 
    
    return render(
        request,
        'posts/feed.html',
        context={ 
            'username': username,
            'posts': posts,
            'countdown': countdown
        } 
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

@login_required
def create_post(request) -> HttpResponse:
    """
    Creates a post from the logged-in user with the specified content.
    """
    if _is_sunday():
        if request.method == "GET":
            form = CreatePostForm()
            return render(request, 'posts/create_post.html', context={ 'form': form })
        elif request.method == "POST":
            form = CreatePostForm(data=request.POST)
            if form.is_valid():
                content = form.cleaned_data["content"] # Use user logged into session as author
                username = request.user.username
                author = ExtendedUser.objects.get(user__username=username)
                Post.objects.create(content=content, author=author)
                return HttpResponseRedirect(reverse('posts:profile', kwargs={'username': username}))
            else:
                # If submitted post is not valid (e.g. exceeds length), return back to form.
                return render(request, 'posts/create_post.html', context={ 'form': form })
        else:
            response = HttpResponse("Unsupported method.", headers = {"Allowed": "GET, POST"})
            response.status_code = 405
            return response
    else:
        return render(request, 'posts/come_back_later.html')

# TO-DO: Migrate user creation to the `registration` app

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
                login(request, user=user)
                return HttpResponseRedirect(reverse('posts:feed'))
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


class ISOWeekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

def _get_day_at(utc_offset) -> ISOWeekday:
    # returns ISO number for day of the week at the timezone specified by its UTC offset
    current_datetime = datetime.now(tz=timezone(timedelta(hours=utc_offset)))
    current_weekday = ISOWeekday(current_datetime.date().isoweekday())
    return current_weekday

def _is_sunday() -> bool:
    kiribati_day = _get_day_at(+14)
    idlw_day = _get_day_at(-12)
    return kiribati_day == ISOWeekday.SUNDAY or idlw_day == ISOWeekday.SUNDAY

def is_sunday(request) -> HttpResponse:
    """
    Returns an HttpResponse with "Yes." if it is Sunday anywhere on Earth,
    with "No." otherwise.
    """
    return HttpResponse("Yes." if _is_sunday() else "No.")