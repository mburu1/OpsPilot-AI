from rest_framework import serializers
from .models import AIInvestigation

class AIInvestigationSerializer(serializers.ModelSerializer):
    incident_title = serializers.ReadOnlyField(source='incident.title')

    class Meta:
        model = AIInvestigation
        fields = '__all__'
