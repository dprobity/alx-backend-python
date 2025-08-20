from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    sent_at__gte = filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    sent_at__lte = filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'sent_at__gte', 'sent_at__lte']
