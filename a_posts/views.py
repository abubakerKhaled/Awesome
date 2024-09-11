from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

from .models import *
from .forms import *


def home_view(request, tag=None):
    posts = Post.objects.filter(tags__slug=tag) if tag else Post.objects.all()

    if tag:
        tag = get_object_or_404(Tag, slug=tag)

    categories = Tag.objects.all()  # Consider prefetching if used often

    context = {
        "posts": posts,
        "categories": categories,
        "tag": tag,
    }
    return render(request, "a_posts/home.html", context)


def find_image(sourcecode):
    try:
        return sourcecode.select_one('meta[content^="https://live.staticflickr.com/"]')[
            "content"
        ]
    except (IndexError, TypeError):
        return None  # Handle missing image


def find_title(sourcecode):
    try:
        return sourcecode.select_one("h1.photo-title").text.strip()
    except (IndexError, TypeError):
        return "Untitled"  # Default title


def find_artist(sourcecode):
    try:
        return sourcecode.select_one("a.owner-name").text.strip()
    except (IndexError, TypeError):
        return "Unknown Artist"  # Default artist


@login_required
def post_create_view(request):
    if request.method == "GET":
        form = PostCreateForm()
    else:
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            try:
                website = requests.get(form.cleaned_data["url"], timeout=10)
                website.raise_for_status()  # Ensure response is OK
                sourcecode = BeautifulSoup(website.content, "lxml")

                post.image = find_image(sourcecode)
                post.title = find_title(sourcecode)
                post.artist = find_artist(sourcecode)

            except (RequestException, AttributeError):
                messages.error(request, "Failed to retrieve data from the URL.")
                return render(request, "a_posts/post_create.html", {"form": form})

            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "Post created successfully.")
            return redirect("a_posts:home")

    return render(request, "a_posts/post_create.html", {"form": form})


@login_required
def post_delete_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect(reverse("a_posts:home"))

    return render(request, "a_posts/post_delete.html", {"post": post})


@login_required
def post_edit_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect(reverse("a_posts:post", args=[post_id]))
    else:
        form = PostEditForm(instance=post)

    return render(request, "a_posts/post_edit.html", {"post": post, "form": form})


def post_page_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    tags = Tag.objects.all()

    comment_form = CommentCreateForm()

    context = {
        'form' : comment_form,
        'post' : post,
        'tags': tags,
    }

    return render(request, "a_posts/post_page.html", context)

@login_required
def comment_sent(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        comment_form = CommentCreateForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.parent_post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect(reverse("a_posts:post", args=[id]))


@login_required
def comment_delete_view(request, id):
    comment = get_object_or_404(Comment, id=id, author=request.user)
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect(reverse("a_posts:post", args=[comment.parent_post.id]))
    context = {
        'post' : comment.parent_post,
        'comment' : comment,
    }
    return render(request, "a_posts/comment_delete.html", context)

@login_required
def reply_sent(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.method == 'POST':
        reply_form = ReplyCreateForm(request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.parent_comment = comment
            new_reply.author = request.user
            new_reply.save()
            messages.success(request, "Reply added successfully.")
            return redirect(reverse("a_posts:post", args=[comment.parent_post.id]))


@login_required
def reply_delete_view(request, id):
    reply = get_object_or_404(Reply, id=id, author=request.user)
    if request.method == "POST":
        reply.delete()
        messages.success(request, "Reply deleted successfully.")
        return redirect(reverse("a_posts:post", args=[reply.parent_comment.parent_post.id]))
    context = {
        "post": reply.parent_comment.parent_post,
        "reply": reply,
    }
    return render(request, "a_posts/reply_delete.html", context)


def like_toggle(model_cls):
    def innerfunc(func):
        def wrapper(request, *args, **kwargs):
            # Get the model instance using the id from kwargs
            model_instance = get_object_or_404(model_cls, id=kwargs.get("id"))
            user_exists = model_instance.likes.filter(
                username=request.user.username
            ).exists()

            # Ensure that the author can't like their own content
            if model_instance.author != request.user:
                if user_exists:
                    model_instance.likes.remove(request.user)
                    messages.success(request, "Unliked")
                else:
                    model_instance.likes.add(request.user)
                    messages.success(request, "Liked post.")

            # Call the decorated function without passing kwargs
            return func(request, model_instance, *args)  # Exclude kwargs

        return wrapper

    return innerfunc


@login_required
@like_toggle(Post)
def like_post(request, model_instance):
    context = {"post": model_instance}
    return render(request, "snippets/likes.html", context)


@login_required
@like_toggle(Comment)
def like_comment(request, model_instance):
    context = {"comment": model_instance}
    return render(request, "snippets/likes_comment.html", context)


@login_required
@like_toggle(Reply)
def like_reply(request, model_instance):
    context = {"reply": model_instance}
    return render(request, "snippets/likes_reply.html", context)
