from django.db import models


class User(models.Model):
    displayName = models.CharField(max_length=150)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=10)
    image = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return f'User: {self.id}'
