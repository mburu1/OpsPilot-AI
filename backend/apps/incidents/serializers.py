from rest_framework import serializers
from .models import Incident

class IncidentSerializer(serializers.ModelSerializer):
    event_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Incident
        fields = '__all__'

    def get_event_count(self, obj):
        return obj.events.count()
