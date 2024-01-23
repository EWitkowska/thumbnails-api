from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Account

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "url"]
        read_only_fields = ["url"]

        extra_kwargs = {
            "url": {"view_name": "users-detail", "lookup_field": "pk"},
        }


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "can_retrieve_original_image", "can_generate_expiring_link"]
