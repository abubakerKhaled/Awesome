from django.contrib import admin
from .models import *

class InboxMessageAdmin(admin.ModelAdmin):
    readonly_fields = ['sender', 'body', 'Conversation']


admin.site.register(InboxMessage, InboxMessageAdmin)
admin.site.register(Conversation)
