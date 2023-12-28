from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с моделью User

    def __str__(self):
        return self.short_url


class CodeState(models.Model):
    last_code = models.CharField(max_length=8, default='aaaaaaaa')

    def __str__(self):
        return self.last_code


class DeletedCode(models.Model):
    code = models.CharField(max_length=8)

    def __str__(self):
        return self.code
