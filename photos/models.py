from __future__ import unicode_literals
from django.db import models
from authentication.models import UserModel


class PostModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    image = models.FileField()
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    has_liked = False

    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post=self))

    @property
    def comments(self):
        return CommentModel.objects.filter(post=self).order_by('-created_on')

    @property
    def categories(self):
        return CategoryModel.objects.filter(post=self)


class LikeModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class CommentModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=555)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class CategoryModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    category_text = models.CharField(max_length=555)
