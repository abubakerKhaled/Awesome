from django.forms import ModelForm
from django import forms
from .models import *


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["url", "body", "tags"]
        labels = {
            'body': 'Caption',
            'tags': 'Category',
        }
        widgets = {
            'url': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Add a URL ...'}),
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a Caption ... ', 'class': 'font1 text-4xl'}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["body", "tags"]
        labels = {
            'body': 'Caption',
            'tags': 'Category'
        }
        widgets = {
            "body": forms.Textarea(
                attrs={"rows": 3, "class": "font1 text-4xl rounded-lg"}
            ),
            "tags": forms.CheckboxSelectMultiple(),
        }

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': ''
        }
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "placeholder": "Add Comment...",
                    "class": "w-full",
                }
            ),
        }


class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        labels = {
            'body': ''
        }
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "placeholder": "Add Reply...",
                    "class": "!text-sm w-full",
                }
            ),
        }
