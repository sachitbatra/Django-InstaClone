from __future__ import unicode_literals
from django.shortcuts import render, redirect
from authentication.views import *
from .models import PostModel, LikeModel, CommentModel, CategoryModel
from .forms import PostForm, LikeForm, CommentForm
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from Instagram.API_KEYS import *


def profile_view(request, email):
    if check_user_token_validation(request):
        user = get_user(request)

    if user is not None:
        user_required = UserModel.objects.filter(email_address=email).first()
        if user_required is None:
            raise Http404
        posts = PostModel.objects.filter(user=user_required).order_by('-created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/')


def tag_view(request, tag_name):
    if check_user_token_validation(request):
        user = get_user(request)

    if user is not None:
        tags = CategoryModel.objects.filter(category_text=tag_name)
        posts = []

        for tag in tags:
            post = tag.post
            posts.append(post)
            existing_like = LikeModel.objects.filter(post_id=tag.post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/')


def post_view(request):
    if request.method == 'POST':
        if check_user_token_validation(request):
            user = get_user(request)
        if user is not None:
            postForm = PostForm(request.POST, request.FILES)
            if postForm.is_valid():
                image = postForm.cleaned_data.get('image')
                caption = postForm.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                add_category(post)
                return redirect('/photos/feed')
            else:
                import pdb
                pdb.set_trace()
                messages.error(request, 'Invalid Data Received')
                return redirect('/photos/feed')
        else:
            return redirect('/')
    else:
        if check_user_token_validation(request):
            user = get_user(request)
            postForm = PostForm()
            return render(request, 'post.html', {'form': postForm})
        else:
            return redirect('/')


def feed_view(request):
    if check_user_token_validation(request):
        user = get_user(request)

    if user is not None:
        posts = PostModel.objects.all().order_by('-created_on')
        postForm = PostForm()

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts, 'form': postForm})
    else:
        return redirect('/')


def like_view(request):
    if check_user_token_validation(request):
        user = get_user(request)

    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/photos/feed')
        else:
            messages.error(request, 'Invalid Data Received')
            return redirect('/photos/feed')
    else:
        return redirect('/')


def view_likes(request, post_id):
    if check_user_token_validation(request):
        user = get_user(request)
    if user is not None:
        curPost = PostModel.objects.filter(id=post_id).first()
        if curPost is None:
            raise Http404

        likes = LikeModel.objects.filter(post=curPost).order_by('-created_on')
        users = []

        for like in likes:
            users.append(like.user)

        return render(request, 'likes.html', {'users': users})

    else:
        return redirect('/')


def comment_view(request):
    if check_user_token_validation(request):
        user = get_user(request)

    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/photos/feed')
        else:
            messages.error(request, 'Invalid Data Received')
            return redirect('/photos/feed')
    else:
        return redirect('/')


def add_category(post):
    app = ClarifaiApp(api_key=API_KEY)
    model = app.models.get("general-v1.3")
    image = ClImage(file_obj=open(post.image.path, 'rb'))
    response = model.predict([image])

    if response["status"]["code"] == 10000:
        if response["outputs"]:
            if response["outputs"][0]["data"]:
                if response["outputs"][0]["data"]["concepts"]:
                    for index in range(0, len(response["outputs"][0]["data"]["concepts"])):
                        category = CategoryModel(post=post, category_text=response["outputs"][0]["data"]["concepts"][index]["name"])
                        category.save()
                else:
                    print("No Concepts List Error")
            else:
                print("No Data List Error")
        else:
            print("No Outputs List Error")
    else:
        print("Response Code Error")
