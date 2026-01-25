from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from tutors.models import Tutors
from .models import Message
from .forms import MessageForm

# Create your views here.


def messaging(request):

    message = Message.objects.all()
    
    my_messages = Message.objects.filter(send_to=User.username)

    message_count = len(my_messages)

    context = {
        'message': message,
        'message_count': message_count,
    }

    return render(request, 'messaging/messaging.html', context)


def compose_message(request, tutor_id):

    compose = get_object_or_404(Tutors, pk=tutor_id)

    if request.method == 'POST':
        form = MessageForm(request.POST, tutor_id)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your message has been\
                             sent to {compose.name}')
            return redirect('tutors')
    
    else:
        form = MessageForm()

    context = {'compose': compose,
               'form': form}

    return render(request, 'messaging/compose-message.html', context)
