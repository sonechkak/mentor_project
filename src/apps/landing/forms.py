from django import forms

from apps.landing.models import AboutMe


class AboutMeForm(forms.ModelForm):
    class Meta:
        model = AboutMe
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control ',
                                                 'placeholder': "Напишите информацию о себе",
                                                 'rows': 3,})}