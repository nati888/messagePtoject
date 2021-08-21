from rest_framework import serializers

from message.models import Message, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "get_full_name"]


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "subject", "message", "creation_date"]


