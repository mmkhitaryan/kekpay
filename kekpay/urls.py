from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .users.views import ObtainChallengeJWT, AttemptChallenge

router = DefaultRouter()

urlpatterns = [
    path('api/auth/obtain/', ObtainChallengeJWT.as_view()),
    path('api/auth/attempt/', AttemptChallenge.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
