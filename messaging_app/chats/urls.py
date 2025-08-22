from django.urls import path, include
from rest_framework import routers

from rest_framework_nested.routers import NestedDefaultRouter
from .views import (
    ConversationViewSet, MessageViewSet, UserRegistrationView, jwt_login, jwt_logout
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

nested = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested.register(r'messages', MessageViewSet, basename='conversation-messages')


urlpatterns = [
    # Auth endpoints (can also be included in a seperate auth app)
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', jwt_login, name='jwt_login'),
    path('logout/', jwt_logout, name='jwt_logout'),


    # JWT token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # Routers
    path('', include(router.urls)),
    path('', include(nested.urls)),
]