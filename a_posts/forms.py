from django.forms import ModelForm
from django import forms
from .models import *


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        labels = {
            'body': 'Caption',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a Caption ... ', 'class': 'font1 text-4xl'}),
        }
        