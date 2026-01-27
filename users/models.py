from django.conf import settings
from django.db import models
from core.models import Franchise

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    franchise = models.ForeignKey(
        Franchise,
        on_delete=models.PROTECT,
        related_name="users"
    )
    role = models.CharField(
        max_length=50,
        choices=[
            ("ADMIN", "Admin"),
            ("MANAGER", "Manager"),
            ("SELLER", "Seller"),
        ]
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Seller(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller"
    )
    franchise = models.ForeignKey(
        Franchise,
        on_delete=models.PROTECT,
        related_name="sellers"
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Seller: {self.user.username}"