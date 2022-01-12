from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firs_name = models.CharField(max_length=150,  null=True)
    last_name = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=150, null=True)
    avatar = models.FileField(upload_to='media/avatars/', null=True, blank=True, default='media/avatars/orange.jpg')

    def __str__(self):
        return f'{self.user}'
