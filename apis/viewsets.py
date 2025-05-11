from rest_framework import routers, viewsets  # Noqa
from django.conf import settings
from .serializers import UserSerializer


# ViewSets define the view behavior.


class UserViewSet(viewsets.ModelViewSet):
    User = settings.AUTH_USER_MODEL

    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
