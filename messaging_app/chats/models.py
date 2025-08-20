from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

# --- Custom User Manager ---
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name="Admin", last_name="Admin", **extra_fields):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# --- Custom User Model ---
class CustomUser(AbstractUser):
    ROLES = (
        ('ADMIN', 'admin'),
        ('GUEST', 'guest'),
        ('HOST', 'host')
    )
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True, null=False, blank=False, verbose_name="Email Address")
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    role = models.CharField(max_length=10, choices=ROLES, default='GUEST')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email as the unique identifier for authentication instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_id']),
        ]
        ordering = ['date_joined']

    def __str__(self):
        return self.email

# --- Conversation Model ---
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    participants = models.ManyToManyField(CustomUser, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['conversation_id'])
        ]
        ordering = ['-created_at']

    def __str__(self):
        names = ", ".join([p.first_name for p in self.participants.all()])
        return f"Conversation {self.conversation_id} ({names})"

# --- Message Model ---
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField(null=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['message_id']),
            models.Index(fields=['conversation']),
        ]
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender.email} in conversation {self.conversation.conversation_id}"
