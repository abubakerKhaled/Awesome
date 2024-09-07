from django.urls import path

from .views import *

app_name = 'a_users'


urlpatterns = [
    path('profile', profile_view, name='profile'),
    path('profile/edit', profile_edit_view, name='profile_edit'),
]