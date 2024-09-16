from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *



@login_required
def inbox_view(request):
    conversation = Conversation.objects.first()
    my_conversations = Conversation.objects.filter(participants=request.user)
    
    context = {
        'conversation': conversation,
        'my_conversations': my_conversations,
    }
    return render(request, 'a_inbox/inbox.html', context)