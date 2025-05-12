from rest_framework import routers, viewsets  # Noqa
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

# ViewSets define the view behavior.


# class UserViewSet(viewsets.ModelViewSet):

#     queryset = get_user_model.objects.all()
#     serializer_class = UserSerializer


