from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *



@login_required
def inbox_view(request, conversation_id=None):
    my_conversations = Conversation.objects.filter(participants=request.user)

    if conversation_id:
        conversation = get_object_or_404(my_conversations, id=conversation_id)    
    else:
        conversation = None
        
    context = {
        'conversation': conversation,
        'my_conversations': my_conversations,
    }
    return render(request, 'a_inbox/inbox.html', context)

def search_users(request):
    letters = request.GET.get('search_user')
    if len(letters) > 0:
        users = User.objects.filter(username__startwith=letters).exclude(username=request.user.username)
        context = {
            'users': users
        }
        return render(request, 'a_inbox/list_search_user.html', context)
    else:
        return HttpResponse('')
        