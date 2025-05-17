# views.py
from rest_framework import generics
from ..models import Workout
from ..serializers import WorkoutSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions.rest_framework import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class WorkoutListCreateView(generics.ListCreateAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["workout_type", "date"]
    search_fields = ["title", "notes"]
    ordering_fields = ["date", "title"]
    permission_classes = [IsAuthenticated, IsAdminUser]


class WorkoutRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workout.objects.all()
    permission_classes = [IsAdminUser, IsOwnerOrReadOnly]
    serializer_class = WorkoutSerializer
