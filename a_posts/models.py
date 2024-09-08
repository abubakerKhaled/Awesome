from django.db import models
from django.contrib.auth.models import User
import uuid

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['order']
        
class Post(models.Model):
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    image = models.URLField(max_length=500)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        if len(self.title) > 50:
            return self.title[:50] + '...'
        return self.title
    
    class Meta:
        ordering = ['-created']
