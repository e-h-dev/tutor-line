from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from tutors.models import Tutors
from .models import Message
from .forms import MessageForm

# Create your views here.


def messaging(request):

    message = Message.objects.all()

    current_user = request.user.username
    
    my_messages = Message.objects.filter(send_to=current_user)

    message_count = len(my_messages)

    print("user is",  request.user.username)

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
            send_mail(
                'Message from Tutor Line',
                f"Dear {compose.name}! \
                        You have recieved a DM from someone reaching\
                            out to you. Check out the message\
                            on your messages page.\
                            Best Regards!\
                            The Tutor Line team.",
                "info@tutor-line.co.uk",
                [compose.email],
                fail_silently=False,
            )
            return redirect('tutors')
    
    else:
        form = MessageForm()

    context = {'compose': compose,
               'form': form}

    return render(request, 'messaging/compose-message.html', context)


def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)

    message.delete()
    messages.success('Message Deleted')
    return redirect(reverse('messaging'))
