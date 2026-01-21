from django.shortcuts import render, get_object_or_404, redirect
from tutors.models import Tutors
from .models import Message
from .forms import MessageForm

# Create your views here.


def messages(request):

    message = Message.objects.all()

    return render(request, 'messaging/messages.html', {'message': message})


def compose_message(request, tutor_id):

    compose = get_object_or_404(Tutors, pk=tutor_id)

    if request.method == 'POST':
        form = MessageForm(request.POST, tutor_id)
        if form.is_valid():
            form.save()
            return redirect('tutors')
    
    else:
        form = MessageForm()

    context = {'compose': compose,
               'form': form}

    return render(request, 'messaging/compose-message.html', context)
