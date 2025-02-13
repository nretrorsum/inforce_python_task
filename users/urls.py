from django.urls import path
from rest_framework.throttling import ScopedRateThrottle
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.TokenObtainPairView.as_view(throttle_classes=[ScopedRateThrottle]),
         name='token_obtain_pair'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('token/refresh/', views.TokenRefreshView.as_view(throttle_classes=[ScopedRateThrottle]),
         name='token_refresh'),    
]