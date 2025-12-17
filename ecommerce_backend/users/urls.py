from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import register_user, user_profile

urlpatterns = [
    # User registration
    path('register/', register_user, name='user-register'),
    
    # User profile
    path('profile/', user_profile, name='user-profile'),
    
    # JWT token endpoints
    path('login/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]