from django.db import models

from core.models import Franchise


class Plan(models.Model):
    TYPE_RESIDENTIAL = "residential"
    TYPE_BUSINESS = "business"
    TYPE_CHOICES = [
        (TYPE_RESIDENTIAL, "Residencial"),
        (TYPE_BUSINESS, "Empresarial"),
    ]

    franchise = models.ForeignKey(
        Franchise,
        on_delete=models.PROTECT,
        related_name="plans",
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    plan_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.franchise.code})"
