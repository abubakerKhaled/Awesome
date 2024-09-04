from django.urls import path

from . import views

app_name = 'a_posts'

urlpatterns = [
    ## Home page
    path('', views.home_view, name='home'),

    ## Create a new post 
    path('post/create/', views.post_create_view, name='create_post')
]
