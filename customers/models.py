from django.db import models

from core.models import Franchise


class Customer(models.Model):
    STATE_PROSPECT = "prospect"
    STATE_ACTIVE = "active"
    STATE_INACTIVE = "inactive"
    STATE_CHOICES = [
        (STATE_PROSPECT, "Prospect"),
        (STATE_ACTIVE, "Active"),
        (STATE_INACTIVE, "Inactive"),
    ]

    franchise = models.ForeignKey(
        Franchise,
        on_delete=models.PROTECT,
        related_name="customers",
    )
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default=STATE_PROSPECT,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.franchise.code})"
