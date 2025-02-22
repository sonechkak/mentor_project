from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from apps.landing.models import MainInf, AboutMe, Content, Product, Point



class AboutMeForm(forms.ModelForm):
    class Meta:
        model = AboutMe
        fields = ['text']


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'image', 'text', 'link', 'link_text']


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'price', 'text']

class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ['text', 'product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'product' in self.initial:
            self.fields['product'].initial = self.initial['product']

PointFormSet = inlineformset_factory(
    Product,  # Родительская модель
    Point,  # Модель для вложенных данных
    form=PointForm,  # Используемая форма
    extra=2,  # Количество пустых форм для заполнения
    can_delete=False,  # Разрешить удаление
)
