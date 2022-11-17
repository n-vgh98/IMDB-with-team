from django import forms
from .models import *


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'avatar']


class CommentForm(forms.ModelForm):
    class Meta:
        model = MovieComment
        fields = ['comment_body']
