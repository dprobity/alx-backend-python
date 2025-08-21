from rest_framework import viewsets, generics, status, filters as drf_filters
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate, logout
from .serializers import (
    UserRegistrationSerializer, LoginSerializer,
    MessageCreateSerializer, MessageDisplaySerializer, ConversationSerializer
)
from .models import Message, Conversation
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipantOfConversation
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication
from .pagination import CustomMessagePagination
from .filters import MessageFilter

CustomUser = get_user_model()

# -- User Registration --
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

# -- Login (JWT) --
@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(request, email=serializer.validated_data['email'], password=serializer.validated_data['password'])
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# -- Logout (JWT) --
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def jwt_logout(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        logout(request)  # Django session logout
        return Response({"detail": "Logged out"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"detail": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

# -- Conversation ViewSet --
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        self.check_object_permissions(request, conversation)
        messages = conversation.messages.all().order_by('-sent_at')
        paginator = CustomMessagePagination()
        result_page = paginator.paginate_queryset(messages, request)
        serializer = MessageDisplaySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

# -- Message ViewSet --
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageDisplaySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    pagination_class = CustomMessagePagination
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']

    def get_queryset(self):
        user = self.request.user
        qs = Message.objects.filter(conversation__participants=user)
        # Optionally, filter by conversation_id in query params
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            qs = qs.filter(conversation__conversation_id=conversation_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request, "user": self.request.user})
        return context
