from django import forms
from .models import Skill


class SkillForm(forms.ModelForm):

    class Meta:

        model = Skill

        fields = [
            'name',
            'description',
            'skill_type'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter skill name'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Describe your skill'
                }
            ),

            'skill_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            )

        }