from django.db import models


class File(models.Model):
    data = models.TextField(null=True)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
