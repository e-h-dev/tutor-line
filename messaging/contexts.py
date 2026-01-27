from .models import Message


def messaging(request):

    message = Message.objects.all()

    current_user = request.user.username
    
    my_messages = Message.objects.filter(send_to=current_user)

    unread_messages = my_messages.filter(read=False)

    message_count = len(my_messages)

    unread_count = len(unread_messages)

    context = {
        'message': message,
        'message_count': message_count,
        'unread_count': unread_count,
    }

    return context
