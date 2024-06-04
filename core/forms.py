from django import forms
from .models import Customer


class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = [
            'image',
            'bio',
            'phone',
            'location'
        ]
