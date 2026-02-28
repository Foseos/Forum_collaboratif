from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Notification

User = get_user_model()


class NotificationSenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "avatar"]


class NotificationSerializer(serializers.ModelSerializer):
    sender = NotificationSenderSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id", "sender", "notification_type", "message",
            "is_read", "target_object_id", "created_at",
        ]
        read_only_fields = ["id", "sender", "notification_type", "message", "created_at"]
