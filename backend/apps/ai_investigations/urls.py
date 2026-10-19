from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIInvestigationViewSet
from .chat_views import AIInvestigationChatViewSet

router = DefaultRouter()
router.register(r'investigations', AIInvestigationViewSet)
router.register(r'chat', AIInvestigationChatViewSet, basename='ai-chat')

urlpatterns = [
    path('', include(router.urls)),
]
