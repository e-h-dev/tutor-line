from django import forms
from .models import Location, Category, Tutors


class TutorForm(forms.ModelForm):

    class Meta:
        model = Tutors
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    