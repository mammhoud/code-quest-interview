# views.py
from rest_framework import generics
from ..models import Stat
from ..serializers import StatSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.permissions import IsOwnerOrReadOnly


class StatListCreateView(generics.ListCreateAPIView):
    """
    List all stats or create a new stat.
    using a filter backend to filter by profile ID or evaluation.
    and order the output by total_records, total_exercises, or evaluation.
    Example: /api/stats/?ordering=total_records
    
    Optionally filter by profile ID or evaluation.
    Example: /api/stats/?profile=3&evaluation=5
    
    """
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["profile", "evaluation"]
    search_fields = ["profile__full_name"]
    ordering_fields = ["total_records", "total_exercises", "evaluation"]
    permission_classes = [IsAuthenticated, IsAdminUser]


class StatRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a stat instance.
    using a permission class to allow only the owner to update or delete their own stats also admin user that created with 
    createsuperuser command.
    """
    queryset = Stat.objects.all()
    permission_classes = [IsAdminUser, IsOwnerOrReadOnly]
    serializer_class = StatSerializer
