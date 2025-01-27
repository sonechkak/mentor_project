from django import forms

from blog.models import Comment


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['html_content']
        widgets = {'html_content': forms.Textarea(attrs={'class': 'form-control custom-textarea',
                                                         'placeholder': "Оставьте свой комментарий",
                                                         'rows': 3,})}
        labels = {'html_content': 'Комментарий'}
