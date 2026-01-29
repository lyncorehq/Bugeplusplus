from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Seller

class MeSerializer(serializers.ModelSerializer):
    franchise = serializers.CharField(source="profile.franchise.name")
    role = serializers.CharField(source="profile.role")

    class Meta:
        model = User
        fields = ["id", "username", "email", "franchise", "role"]


class SellerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Seller
        fields = ["id", "username", "email", "is_active"]
        read_only_fields = ["username", "email"]
