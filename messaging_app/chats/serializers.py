from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    # Explicitly declare Charfield for username (even though ModelSerialzer does this authomatically)
    username = serializers.Charfield()
    class Meta:
        model = User
        fileds = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at', 'preview']

    def get_preview(self, obj):
        # Provide a short preview of the message body (first 20 chars)
        return obj.message_body[:20]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']


    # Custom validation, checking if conversation have atleast two participants
    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have atleast two particpants")
        return value