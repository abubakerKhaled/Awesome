from django.db import models
import uuid

class Post(models.Model):
    title = models.CharField(max_length=500)
    image = models.URLField(max_length=500)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        if len(self.title) > 50:
            return self.title[:50] + '...'
        return self.title
    
    class Meta:
        ordering = ['-created']
