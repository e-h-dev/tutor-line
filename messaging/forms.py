from django import forms
from .models import Message
# from django.contrib.auth.models import User


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

