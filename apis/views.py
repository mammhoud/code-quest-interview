from rest_framework.generics import ListCreateAPIView
from .models import Stat
from .serializers import StatSerializer


class StatsListCreateView(ListCreateAPIView):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
