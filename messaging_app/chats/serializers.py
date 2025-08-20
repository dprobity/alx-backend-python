from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

CustomUser = get_user_model()


# --- USER REGISTRATION & OUTPUT SERIALIZER ---
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=7)
    confirm_password = serializers.CharField(write_only=True, min_length=7)
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'user_id', 'email', 'first_name', 'last_name',
            'password', 'confirm_password', 'phone_number', 'role', 'full_name'
        ]
        read_only_fields = ['user_id', 'role', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number'),
            role=validated_data.get('role', 'GUEST')
        )
        return user


class UserDisplaySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'user_id', 'email', 'first_name', 'last_name',
            'phone_number', 'role', 'full_name', 'created_at'
        ]
        read_only_fields = fields

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


# --- LOGIN SERIALIZER ---
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=7)


# --- CONVERSATION SERIALIZER ---
class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.all()
    )
    messages = serializers.SerializerMethodField(read_only=True)
    conversation_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
        read_only_fields = ['conversation_id', 'created_at', 'messages']

    def get_messages(self, obj):
        # Return latest 10 messages (or all if <10)
        messages = obj.messages.order_by('-sent_at')[:10][::-1]
        return MessageDisplaySerializer(messages, many=True).data

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least two participants."
            )
        return value

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation

    def update(self, instance, validated_data):
        if 'participants' in validated_data:
            instance.participants.set(validated_data['participants'])
        instance.save()
        return instance


# --- MESSAGE SERIALIZER (for creation) ---
class MessageCreateSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation_id', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sender', 'sent_at']

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user if request else None
        conversation_id = attrs.get('conversation_id')
        message_body = attrs.get('message_body', '')

        # Check for empty body
        if not message_body or not message_body.strip():
            raise serializers.ValidationError("Message body cannot be empty.")

        # Validate conversation exists
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation does not exist.")

        # User must be a participant
        if not conversation.participants.filter(pk=user.pk).exists():
            raise serializers.ValidationError("You are not a participant of this conversation.")

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        conversation_id = validated_data.pop('conversation_id')
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        message = Message.objects.create(
            sender=user,
            conversation=conversation,
            message_body=validated_data['message_body']
        )
        return message


# --- MESSAGE DISPLAY SERIALIZER ---
class MessageDisplaySerializer(serializers.ModelSerializer):
    sender = UserDisplaySerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'message_body',
            'conversation', 'sent_at'
        ]
        read_only_fields = fields

