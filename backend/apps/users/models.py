from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrateur"
        MODERATOR = "moderator", "Modérateur"
        USER = "user", "Utilisateur"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role in (self.Role.ADMIN, self.Role.MODERATOR)
