from django.urls import path, include

urlpatterns = [
    path('api/services/', include('apps.services.urls')),
    path('api/events/', include('apps.events.urls')),
    path('api/correlations/', include('apps.correlations.urls')),
    path('api/incidents/', include('apps.incidents.urls')),
    path('api/investigations/', include('apps.ai_investigations.urls')),
]
