from django.db import models
from user.models import User


class Post(models.Model):
    title = models.TextField()
    content = models.TextField()
    user = models.ForeignKey(User, related_name='post', on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Post: {self.id}'
