from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CorrelationRuleViewSet

router = DefaultRouter()
router.register(r'rules', CorrelationRuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
