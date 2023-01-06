from rest_framework import serializers
from .models import Wcapi



class WcapiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wcapi
        fields = ('user_id', 'number', 'is_parser')