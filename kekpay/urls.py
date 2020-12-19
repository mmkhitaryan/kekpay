from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenRefreshView

from .users.views import ObtainChallengeJWT, AttemptChallenge

router = DefaultRouter()

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/obtain/', ObtainChallengeJWT.as_view(), name='obtain-token'),
    path('api/auth/attempt/', AttemptChallenge.as_view(), name='attempt-challenge'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
