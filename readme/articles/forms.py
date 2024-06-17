# blog/forms.py

from django import forms
from .models import Post

class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'authors', 'issues', 'categories', 'body', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'authors': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'issues': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }