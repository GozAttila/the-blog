from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('User', 'User'),
        ('Blogger', 'Blogger'),
        ('Moderator', 'Moderator'),
        ('Subadmin', 'Subadmin'),
        ('Admin', 'Admin'),
    ]
    email = models.EmailField(unique=True)
    avatar = models.URLField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.username
