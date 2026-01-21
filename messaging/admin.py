from django.contrib import admin
from .models import Message

# Register your models here.

class MessagesAdmin(admin.ModelAdmin):
    list_display = (
        'tutor_name',
        'name'
    )


admin.site.register(Message, MessagesAdmin)
