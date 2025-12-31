from django import forms
from .models import Location, Category, Tutors, Reviews


class TutorForm(forms.ModelForm):

    class Meta:
        model = Tutors
        fields = '__all__'
        widgets = {
            'is_male': forms.Select(choices=[
                (None, 'Gender...'),
                (True, 'Male'),
                (False, 'Female'),
            ])
        }

    image = forms.ImageField(label='Image', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RatingForm(forms.ModelForm):

    class Meta:
        model = Tutors
        fields = ('rating',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
