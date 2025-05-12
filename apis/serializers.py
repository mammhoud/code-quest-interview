

from rest_framework import serializers

from core.serializers import ProfileSerializer
from .models import Stat

class StatSerializer(serializers.ModelSerializer):
    full_name = ProfileSerializer(read_only=True)


    class Meta:
        model = Stat
        fields = [
            'id',
            'profile',
            'full_name',
            'total_records',
            'total_exercises',
            'total_friends',
            'evaluation',
        ]
        read_only_fields = ['id', 'full_name']
