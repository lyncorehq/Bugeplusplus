from rest_framework import serializers

from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ["id", "customer", "plan", "state", "created_at"]
        read_only_fields = ["id", "state", "created_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        profile = getattr(request.user, "profile", None)
        if profile is None:
            return attrs

        customer = attrs.get("customer") or getattr(self.instance, "customer", None)
        plan = attrs.get("plan") or getattr(self.instance, "plan", None)

        if customer and customer.franchise_id != profile.franchise_id:
            raise serializers.ValidationError("El cliente no pertenece a tu franquicia.")
        if plan and plan.franchise_id != profile.franchise_id:
            raise serializers.ValidationError("El plan no pertenece a tu franquicia.")
        if plan and not plan.is_active:
            raise serializers.ValidationError("No se puede contratar un plan inactivo.")
        if customer and plan and customer.franchise_id != plan.franchise_id:
            raise serializers.ValidationError("Cliente y plan deben pertenecer a la misma franquicia.")

        return attrs


class ContractStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ["state"]

    def validate_state(self, value):
        instance = self.instance
        if instance and not Contract.can_transition(instance.state, value):
            raise serializers.ValidationError("Transición de estado no permitida.")
        return value
