from django.urls import path

from . import views

app_name = 'a_posts'

urlpatterns = [
    path('', views.home_view, name='home'),
]
