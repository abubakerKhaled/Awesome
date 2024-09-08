from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import Http404
from .forms import ProfileForm


@login_required
def profile_view(request, username=None):
    # Fetch the profile for the provided username or the current user
    user = get_object_or_404(User, username=username) if username else request.user
    profile = getattr(user, "profile", None)

    if not profile:
        raise Http404("Profile not found.")

    context = {"profile": profile}
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
            return redirect("a_users:profile", username=request.user.username)
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
