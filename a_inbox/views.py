from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.db.models import Q
from .models import *
from .forms import *
from a_users.models import Profile


@login_required
def inbox_view(request, conversation_id=None):
    my_conversations = Conversation.objects.filter(participants=request.user)

    if conversation_id:
        conversation = get_object_or_404(my_conversations, id=conversation_id)    
        latest_message = conversation.messages.first()
        if conversation.is_seen == False and latest_message.sender != request.user:
            conversation.is_seen = True
            conversation.save()
    else:
        conversation = None
        
    context = {
        'conversation': conversation,
        'my_conversations': my_conversations,
    }
    return render(request, 'a_inbox/inbox.html', context)



def search_users(request):
    letters = request.GET.get('search_user')
    if request.htmx:
        if len(letters) > 0:
            profiles = Profile.objects.filter(realname__icontains=letters).exclude(realname=request.user.profile.realname)
            users_id = profiles.values_list('user', flat=True)
            users = User.objects.filter(
                Q(username__icontains=letters) | Q(id__in=users_id)
            ).exclude(username=request.user.username)
            context = {
                'users': users,
            }
            return render(request, 'a_inbox/list_search_user.html', context)
        else:
            return HttpResponse('')
    else:
        raise Http404()
    
    
@login_required
def new_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    
    if request.method == 'POST':
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message_body = form.cleaned_data['body']
            
            # Check if a conversation already exists
            conversation = Conversation.objects.filter(
                participants=request.user
            ).filter(
                participants=recipient
            ).first()
            
            if not conversation:
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, recipient)
            
            # Create and save the message
            message = InboxMessage.objects.create(
                sender=request.user,
                Conversation=conversation,
                body=message_body
            )
            
            # Update the conversation using the message's timestamp
            conversation.lastmessage_created = message.created_at
            conversation.is_seen = False
            conversation.save()
            
            return redirect('a_inbox:inbox', conversation.id)
    else:
        form = InboxNewMessageForm()
    
    context = {
        'recipient': recipient,
        'new_message_form': form,
    }
    return render(request, 'a_inbox/form_new_message.html', context)


@login_required
def new_reply(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    if request.method == 'POST':
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message_body = form.cleaned_data['body']
            
            # Create and save the message
            message = InboxMessage.objects.create(
                sender=request.user,
                Conversation=conversation,  # Note the capital 'C' to match your model
                body=message_body
            )
            
            # Update the conversation
            conversation.lastmessage_created = message.created_at
            conversation.is_seen = False
            conversation.save()
            
            return redirect('a_inbox:inbox', conversation.id)
    else:
        form = InboxNewMessageForm()
    
    context = {
        'new_message_form': form,
        'conversation': conversation,
    }
    return render(request, 'a_inbox/form_newreply.html', context)

def notify_newmessage(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    latest_message = conversation.messages.first()
    if conversation.is_seen == False and latest_message.sender != request.user:
        return render(request, 'a_inbox/notify_icon.html')
    return HttpResponse('')