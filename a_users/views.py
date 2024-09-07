from django.shortcuts import render, redirect

from .forms import ProfileForm

def profile_view(request):
    profile = request.user.profile
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
