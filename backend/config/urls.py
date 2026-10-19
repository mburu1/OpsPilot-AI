from django.urls import path, include

urlpatterns = [
    path('api/services/', include('apps.services.urls')),
    path('api/events/', include('apps.events.urls')),
]
