from django.urls import path

from .views import *

app_name = "a_inbox"

urlpatterns = [
    path('', inbox_view, name='inbox')
]

