from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from bs4 import BeautifulSoup
import requests

from .models import *
from .forms import *


def home_view(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()

    categories = Tag.objects.all()
    
    context = {
        "posts": posts,
        "categories": categories,
        'tag': tag,
        }
    return render(request, 'a_posts/home.html', context)


def find_image(sourcecode):
    find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
    return find_image[0]['content']

def find_title(sourcecode):
    find_title = sourcecode.select('h1.photo-title')
    return find_title[0].text.strip()

def find_artist(sourcecode):
    find_artist = sourcecode.select("a.owner-name")
    return find_artist[0].text.strip()


def post_create_view(request):
    if request.method == 'GET':
        form = PostCreateForm()
        return render(request, 'a_posts/post_create.html', {'form': form})
    else:
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.content, 'lxml')

            ## Find the image
            post.image = find_image(sourcecode)

            ## Find the title
            post.title = find_title(sourcecode)

            ## Find the artist
            post.artist = find_artist(sourcecode)
            
            ## Assign the author
            post.author = request.user

            post.save()
            form.save_m2m()
            return redirect('a_posts:home')
        return render(request, 'a_posts/post_create.html', {'form': form})


def post_delete_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'GET': 
        if request.user == post.author:
            context = {'post': post}
        else:
            messages.error(request, "You are not authorized to delete this post.")
            return redirect(reverse_lazy("a_posts:home"))
        return render(request, 'a_posts/post_delete.html', context)
    else:
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect(reverse_lazy('a_posts:home'))

def post_edit_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'GET':
        if request.user == post.author:
            form = PostEditForm(instance=post)
            context = {'post': post, 'form': form}
        else:
            messages.error(request, 'You are not authorized to edit this post.')
            return redirect(reverse_lazy("a_posts:home"))
    else:
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect(reverse_lazy("a_posts:home"))
        context = {'post': post, 'form': form}
    return render(request, 'a_posts/post_edit.html', context)

def post_page_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
    return render(request, 'a_posts/post_page.html', context)
