from django.db import models

from core.models import Franchise


class Customer(models.Model):
    franchise = models.ForeignKey(
        Franchise,
        on_delete=models.PROTECT,
        related_name="customers",
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.franchise.code})"
