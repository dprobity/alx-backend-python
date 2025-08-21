from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import (
    UserRegistrationView, jwt_login, jwt_logout,
    ConversationViewSet, MessageViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth endpoints
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', jwt_login, name='jwt_login'),
    path('api/logout/', jwt_logout, name='jwt_logout'),

    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),     # Alt login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Main API
    path('api/', include(router.urls)),
]
