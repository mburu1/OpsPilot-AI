from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')

    class Meta:
        model = Event
        fields = '__all__'
