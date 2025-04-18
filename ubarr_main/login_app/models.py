from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_group', 
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permission',  
        blank=True,
        help_text='Specific permissions for this user.'
    )
