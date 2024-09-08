from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.utils import timezone
import os

def get_profile_image_path(instance, filename):
    # Ensures unique filenames based on the primary key
    return os.path.join("avatars", f"{instance.pk}_{filename}")

GANDER = ('MALE', 'FEMALE')

class Profile(models.Model):

    class GenderChoices(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    realname = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to=get_profile_image_path, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    gender = models.CharField(
        max_length=6, choices=GenderChoices.choices, null=True, blank=True
    )

    def __str__(self):
        return str(self.user)

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static("images/avatar_default.svg")
        return avatar

    @property
    def name(self):
        if self.realname:
            name = self.realname
        else:
            name = self.user.username
        return name