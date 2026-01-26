from .models import Message


def messaging(request):

    message = Message.objects.all()

    current_user = request.user.username
    
    my_messages = Message.objects.filter(send_to=current_user)

    message_count = len(my_messages)

    context = {
        'message': message,
        'message_count': message_count,
    }

    return context
