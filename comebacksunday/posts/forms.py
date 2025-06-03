from django.forms import ModelForm
from .models import Post

class CreatePostForm(ModelForm):
    """
    To create a post given the content it should contain.
    """
    class Meta:
        model = Post
        fields = ['content']
