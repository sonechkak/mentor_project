from django import forms

from blog.models import Comment


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['html_content']