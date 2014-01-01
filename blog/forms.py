from django import forms
from blog.models import Post

class BookForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('slug', 'publish', 'creator')

