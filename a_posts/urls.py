from django.urls import path

from .views import *

app_name = "a_posts"

urlpatterns = [
    ## Home page
    path("", home_view, name="home"),
    ## Create a new post
    path("post/create/", post_create_view, name="create_post"),
    ## All posts of a given tag (use a 'tag' prefix to differentiate)
    path("tag/<slug:tag>/", home_view, name="category"),
    ## Delete a post
    path("post/delete/<uuid:post_id>/", post_delete_view, name="delete_post"),
    ## Edit a post
    path("post/edit/<uuid:post_id>/", post_edit_view, name="edit_post"),
    ## Post page view
    path("post/<uuid:post_id>/", post_page_view, name="post"),
]
