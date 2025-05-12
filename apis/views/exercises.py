# views.py
from rest_framework import generics
from ..models import Exercise
from ..serializers import ExerciseSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.permissions import IsOwnerOrReadOnly

class ExerciseListCreateView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Optionally filter exercises by profile ID (flexible API)
        Example: /api/exercises/?profile=3
        """
        queryset = super().get_queryset()
        profile_id = self.request.query_params.get("profile")
        if profile_id:
            queryset = queryset.filter(profile_id=profile_id)
        return queryset


class ExerciseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    permission_classes = [IsAdminUser, IsOwnerOrReadOnly]
    serializer_class = ExerciseSerializer
