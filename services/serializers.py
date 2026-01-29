from rest_framework import serializers

from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "price", "plan_type", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]
