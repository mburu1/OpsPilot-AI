from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KnowledgeArticleViewSet

router = DefaultRouter()
router.register(r'articles', KnowledgeArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
