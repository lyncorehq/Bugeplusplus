from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from .models import Seller, UserProfile


ROLE_PERMISSIONS = {
    UserProfile.ROLE_ADMIN: ["*"],
    UserProfile.ROLE_MANAGER: [
        "clients.view",
        "clients.create",
        "clients.update",
        "contracts.view",
        "contracts.create",
        "contracts.update",
        "contracts.change_state",
        "sellers.view",
        "sellers.create",
        "sellers.update",
        "sellers.toggle",
    ],
    UserProfile.ROLE_SELLER: [
        "clients.view",
        "clients.create",
        "clients.update",
        "contracts.view",
        "contracts.create",
        "contracts.update",
    ],
}

class MeSerializer(serializers.ModelSerializer):
    franchise = serializers.CharField(source="profile.franchise.name")
    role = serializers.CharField(source="profile.role")
    full_name = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "full_name", "franchise", "role", "permissions"]

    def get_full_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name or obj.username

    def get_permissions(self, obj):
        role = getattr(obj.profile, "role", None)
        return ROLE_PERMISSIONS.get(role, [])


class SellerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Seller
        fields = ["id", "username", "email", "is_active"]
        read_only_fields = ["username", "email"]


class SellerCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Seller
        fields = ["id", "username", "email", "password", "first_name", "last_name", "is_active"]
        read_only_fields = ["id"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("El username ya está en uso.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("El email ya está en uso.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")
        is_active = validated_data.get("is_active", True)
        franchise = validated_data.pop("franchise")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_active = is_active
        user.save(update_fields=["is_active"])

        UserProfile.objects.create(
            user=user,
            franchise=franchise,
            role=UserProfile.ROLE_SELLER,
        )

        seller = Seller.objects.create(
            user=user,
            franchise=franchise,
            is_active=is_active,
        )
        return seller


class SellerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["is_active"]

    def update(self, instance, validated_data):
        is_active = validated_data.get("is_active", instance.is_active)
        instance.is_active = is_active
        instance.save(update_fields=["is_active"])
        if instance.user.is_active != is_active:
            instance.user.is_active = is_active
            instance.user.save(update_fields=["is_active"])
        return instance
