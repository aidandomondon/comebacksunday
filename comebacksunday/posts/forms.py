from django.forms import Form
from .models import Post
from django.forms import CharField, Textarea

class CreatePostForm(Form):
    """
    To create a post given the content it should contain.
    """
    content = CharField(max_length=Post.content.max_length, widget=Textarea)