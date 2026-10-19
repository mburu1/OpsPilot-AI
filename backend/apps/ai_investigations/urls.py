from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIInvestigationViewSet

router = DefaultRouter()
router.register(r'investigations', AIInvestigationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
