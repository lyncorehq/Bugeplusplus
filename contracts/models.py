from django.db import models

from core.models import Franchise
from customers.models import Customer
from services.models import Plan


class Contract(models.Model):
    STATE_PENDING = "pending"
    STATE_ACTIVE = "active"
    STATE_SUSPENDED = "suspended"
    STATE_CANCELLED = "cancelled"
    STATE_CHOICES = [
        (STATE_PENDING, "Pending"),
        (STATE_ACTIVE, "Active"),
        (STATE_SUSPENDED, "Suspended"),
        (STATE_CANCELLED, "Cancelled"),
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
        default=STATE_PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contract {self.id} ({self.franchise.code})"

    @classmethod
    def can_transition(cls, current_state, next_state):
        transitions = {
            cls.STATE_PENDING: {cls.STATE_ACTIVE, cls.STATE_CANCELLED},
            cls.STATE_ACTIVE: {cls.STATE_SUSPENDED, cls.STATE_CANCELLED},
            cls.STATE_SUSPENDED: {cls.STATE_ACTIVE, cls.STATE_CANCELLED},
            cls.STATE_CANCELLED: set(),
        }
        return next_state in transitions.get(current_state, set())
