from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.db.models import Count
from .forms import ProfileForm
from a_posts.models import Post
from a_posts.forms import ReplyCreateForm


@login_required
def profile_view(request, username=None):
    # Fetch the profile for the provided username or the current user
    user = get_object_or_404(User, username=username) if username else request.user
    profile = getattr(user, "profile", None)
    posts = profile.user.posts.all()

    if not profile:
        raise Http404("Profile not found.")

    if request.htmx:
        if "top-posts" in request.GET:
            # Filter posts with at least one like
            posts = (
                profile.user.posts.annotate(num_likes=Count("likes"))
                .filter(num_likes__gt=0)
                .order_by("-num_likes")
            )

        elif "top-comments" in request.GET:
            # Filter comments with at least one like
            comments = (
                profile.user.comments.annotate(num_likes=Count("likes"))
                .filter(num_likes__gt=0)
                .order_by("-num_likes")
            )
            reply_form = ReplyCreateForm()
            context = {
                "comments": comments,
                "form": reply_form,
            }
            return render(
                request, "snippets/loop_profile_comments.html", context, 
            )
        elif "liked-posts" in request.GET:
            # Fetch posts liked by the user
            posts = Post.objects.filter(likes=request.user).order_by(
                "-likedpost__created_at"
            )
        return render(request, "snippets/loop_profile_posts.html", {"posts": posts})
            

    # Fallback for both HTMX and non-HTMX full profile views
    context = {"profile": profile, "posts": posts}
    
    # Return full profile view for non-HTMX or regular requests
    return render(request, "a_users/profile.html", context)



@login_required
def profile_edit_view(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(
            request.POST, request.FILES, instance=profile
        )  # Handle file uploads (like profile images)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("a_users:user_profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    context = {"form": form}
    return render(request, "a_users/profile_edit.html", context)


@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        # Logout the user before deleting the account
        logout(request)
        user.delete()
        messages.success(
            request, "Your account has been deleted. We’re sorry to see you go."
        )
        return redirect("a_posts:home")

    return render(request, "a_users/profile_delete.html")


@login_required
def profile_onboarding(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(
            request.POST, request.FILES, instance=profile
        )  # Handle file uploads (like profile images)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("a_posts:home")
    else:
        form = ProfileForm(instance=profile)

    context = {"form": form}
    return render(request, "a_users/profile_onboarding.html", context)
