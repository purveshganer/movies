from django.db import models

# Create your models here.
class User(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField(unique=True, max_length=255, db_index=True)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=30, db_index=True)

