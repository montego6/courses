from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class TeacherProfile(models.Model):
    avatar = models.ImageField(upload_to='media/profiles/avatars/')
    bio = models.CharField(max_length=2000)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f'Profile for user id={self.user.id}'