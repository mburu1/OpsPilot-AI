from rest_framework import serializers
from .models import CorrelationRule

class CorrelationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrelationRule
        fields = '__all__'
