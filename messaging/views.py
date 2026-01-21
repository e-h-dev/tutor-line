from django.shortcuts import render, get_object_or_404
from .models import Message

# Create your views here.


def messages(request):

    message = Message.objects.all()

    return render(request, 'messaging/messages.html', {'message': message})
