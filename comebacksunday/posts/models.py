from django.db import models

class User(models.Model):
    """
    Represents a user of the website.
    """
    username = models.CharField(primary_key=True, unique=True, max_length=75)
    bio = models.TextField(max_length=100, verbose_name="Short self-description of user.")
    following = models.ManyToManyField(
        "self", 
        symmetrical=False, 
        related_name="followers",
        verbose_name="Users this user is following."
    )

    # For private accounts
    private = models.BooleanField(
        default=False, 
        verbose_name="Only followers can see this user's posts?"
    )
    requested_followers = models.ManyToManyField(
        "self", 
        symmetrical=False, 
        related_name="+",
        verbose_name="Users with pending requests to follow this user"
    )

    def __str__(self):
        return self.username


class Post(models.Model):
    """
    Represents a post made by a user.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author of this post")
    content = models.TextField(max_length=280)
    datetime = models.DateTimeField(
        auto_now_add=True, # automatically use the date of this row's creation as this row's datetime
        verbose_name="Date and time this post was made."
    )

    def __str__(self):
        return self.author.__str__() + str(self.id)
