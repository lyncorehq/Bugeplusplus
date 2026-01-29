from django.db import models

from core.models import Franchise
from customers.models import Customer
from services.models import Plan


class Contract(models.Model):
    STATE_POR_INSTALAR = "por_instalar"
    STATE_ACTIVO = "activo"
    STATE_SUSPENDIDO = "suspendido"
    STATE_CANCELADO = "cancelado"
    STATE_CHOICES = [
        (STATE_POR_INSTALAR, "Por instalar"),
        (STATE_ACTIVO, "Activo"),
        (STATE_SUSPENDIDO, "Suspendido"),
        (STATE_CANCELADO, "Cancelado"),
    ]

    franchise = models.ForeignKey(
        Franchise,
        on_delete=models.PROTECT,
        related_name="contracts",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="contracts",
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name="contracts",
    )
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default=STATE_POR_INSTALAR,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contract {self.id} ({self.franchise.code})"
