from django import forms

from core import models
from core.models import Pet, Service, GalleryImage


class PetCreateForm(forms.ModelForm):
    image = forms.FileField(
        label='Фото питомца',
        required=False,
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Pet
        fields = [
            'image',
            'pet_type',
            'name',
            'breed',
            'age',
            'weight',
            'extra_info'
        ]


class PetForm(forms.ModelForm):
    WEIGHT = [
        ('1-5 кг', '1-5 кг'),
        ('6-10 кг', '6-10 кг'),
        ('11-20 кг', '11-20 кг'),
        ('21+ кг', '21+ кг')
    ]

    AGE = [
        ('до 1 года', 'до 1 года'),
        ('1 - 5 лет', '1 - 5 лет'),
        ('5 - 8 лет', '5 - 8 лет'),
        ('старше 8 лет', 'старше 8 лет')
    ]

    image = forms.FileField(
        label='Фото питомца',
        required=False,
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'class': 'form-control',
            }
        )
    )

    age = forms.ChoiceField(choices=AGE, widget=forms.Select())

    weight = forms.ChoiceField(choices=WEIGHT, widget=forms.Select())

    extra_info = forms.CharField(
        max_length=500,
        required=False,
        label='Дополнительная информация',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        model = models.Pet
        fields = ['image', 'age', 'weight', 'extra_info']


class AddServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'category',
            'description',
            'price',
        ]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UploadImageForm(forms.ModelForm):
    images = MultipleFileField(widget=MultipleFileInput())

    class Meta:
        model = GalleryImage
        fields = ('images',)
