from django.forms import ModelForm
from django import forms
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "realname", "email", "location", "bio", "gender"]
        labels = {
            "image": "Image",  # Capitalized for consistency
            "realname": "Name",  # Corrected typo
            "email": "Email",
            "location": "Location",
            "bio": "Bio",
            "gender": "Gender",
        }
        widgets = {
            "image": forms.FileInput(),  # Corrected field name
            "bio": forms.Textarea(attrs={"rows": 3}),
        }
