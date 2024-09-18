from django.urls import path

from .views import *

app_name = "a_inbox"

urlpatterns = [ 
    path('', inbox_view, name='inbox'),
    path('conversation/<uuid:conversation_id>', inbox_view, name='inbox'),
    path('search_users/', search_users, name='search_users'),
    path('new_message/<recipient_id>', new_message, name='inbox_new_message'),
    path('new_reply/<conversation_id>', new_reply, name='inbox_newreply'),
    path('notify/<conversation_id>', notify_newmessage, name='notify_newmessage'),
    path('notify/inbox/', notify_inbox, name='notify_inbox'),
]

