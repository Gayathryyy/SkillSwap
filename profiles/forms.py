from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            'phone',
            'location',
            'bio',
            'profile_picture'
        ]

        widgets = {
            'phone': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'location': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),
        }