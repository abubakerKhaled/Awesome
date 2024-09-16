from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("a_posts.urls", namespace="a_posts")),  # Prefixed with 'posts/'
    path("", include("a_users.urls", namespace="a_users")),  # Prefixed with 'users/'
    path("a_inbox/", include("a_inbox.urls", namespace="a_inbox")),  # Prefixed with 'inbox/'
]

# Serving media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
