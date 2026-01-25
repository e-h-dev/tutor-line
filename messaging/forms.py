from django import forms
from .models import Message
# from django.contrib.auth.models import User


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'
        # fields = ['send_to', 'name', 'Phone', 'email', 'message']
        # widgets = {
        #     'send_to': forms.TextInput(attrs={'value': 'RebbeGreen'}),
        #     'name': forms.TextInput(attrs={'placeholder': "Your Name"}),
        #     'Phone': forms.TextInput(attrs={'placeholder': "Your Phone Number"}),
        #     'email': forms.EmailInput(attrs={'placeholder': "Your Email"}),
        #     'message': forms.Textarea(attrs={'placeholder': "Your Message"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

