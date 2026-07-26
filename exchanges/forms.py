from django import forms
from .models import SkillExchange


class SkillExchangeForm(forms.ModelForm):

    class Meta:

        model = SkillExchange

        fields = [

            'skill_requested',

            'skill_offered',

            'message'

        ]

        widgets = {

            'message': forms.Textarea(

                attrs={

                    'rows': 4,

                    'placeholder': 'Write a message...'

                }

            )

        }