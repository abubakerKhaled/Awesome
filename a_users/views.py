from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.http import Http404
from .forms import ProfileForm

def profile_view(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
        profile = user.profile
        context = {"profile": profile}
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
        context = {'profile': profile}
    return render(request, 'a_users/profile.html', context)


def profile_edit_view(request):
    if request.method == "GET":
        form = ProfileForm(instance=request.user.profile)
    else:
        form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )  # Added request.FILES for image uploads
        if form.is_valid():
            form.save()
            return redirect("a_users:profile")  # Redirect after successful form submission

    context = {"form": form}
    return render(
        request, "a_users/profile_edit.html", context
    )  # Render form with errors (if any)

def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('a_posts:home')
    return render(request, "a_users/profile_delete.html")