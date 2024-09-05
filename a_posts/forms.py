from django.forms import ModelForm
from django import forms
from .models import *


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["url", "body"]
        labels = {
            'body': 'Caption',
        }
        widgets = {
            'url': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Add a URL ...'}),
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a Caption ... ', 'class': 'font1 text-4xl'}),
        }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["body"]
        labels = {
            'body': 'Caption',
        }
        widgets = {
            "body": forms.Textarea(
                attrs={"rows": 3, "class": "font1 text-4xl rounded-lg"}
            ),
        }
