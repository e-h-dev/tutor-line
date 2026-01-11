from django import forms
from .models import Location, Category, Tutors, Reviews


class TutorForm(forms.ModelForm):

    class Meta:
        model = Tutors
        fields = ['name', 'location', 'category', 'subject', 'price', 'phone', 'email', 'description', 'is_male']
        widgets = {
            'is_male': forms.Select(choices=[
                (None, 'Are you Male or Female?'),
                (True, 'Male'),
                (False, 'Female'),
            ]),
            'name': forms.TextInput(attrs={'placeholder': "Your Name"}),
            'subject': forms.TextInput(attrs={'placeholder': "Your Subject"}),
            'price': forms.NumberInput(attrs={'placeholder': "Your hourly rate"}),
            'phone': forms.TextInput(attrs={'placeholder': "Your Phone Number"}),
            'email': forms.EmailInput(attrs={'placeholder': "Your Email"}),
            'description': forms.Textarea(attrs={'placeholder': "Your Description"}),

        }

    # image = forms.ImageField(label='Image', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TutorImageForm(forms.ModelForm):
    class Meta:
        model = Tutors
        fields = ['image',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True


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
