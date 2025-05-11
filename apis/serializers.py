# from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets  # Noqa
from django.conf import settings  # Noqa


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        User = settings.AUTH_USER_MODEL
        model = User
        fields = ["url", "username", "email", "is_staff"]
