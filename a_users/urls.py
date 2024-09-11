from django.urls import path
from .views import *

app_name = "a_users"

urlpatterns = [
    ## Logged-in user's profile
    path("profile/", profile_view, name="profile"),
    ## Other users' profiles
    path("user/<str:username>/", profile_view, name="user_profile"),
    ## Edit profile
    path("profile/edit/", profile_edit_view, name="profile_edit"),
    ## Delete profile
    path("profile/delete/", profile_delete_view, name="profile_delete"),
    ## Onboarding Page
    path("profile_onboarding/", profile_onboarding, name="profile_onboarding"),
]
