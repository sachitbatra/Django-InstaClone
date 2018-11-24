from django import forms
from .models import PostModel, LikeModel, CommentModel


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['image', 'caption']


class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields = ['post']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post']
