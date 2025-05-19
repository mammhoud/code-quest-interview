import django_filters
from .models import *



class ExerciseFilter(django_filters.FilterSet):
    """
    Filter for Exercise model.
    """

    class Meta:
        model = Exercise
        fields = {
            "name": ["exact", "icontains"],
            "description": ["exact", "icontains"],
            "duration": ["exact", "gte", "lte"],
            "profile": ["exact"],
        }
        exclude = ["id", "created_at", "updated_at"]


class WorkoutFilter(django_filters.FilterSet):
    """
    Filter for Workout model.
    """

    class Meta:
        model = Workout
        fields = {
            "title": ["exact", "icontains"],
            "date": ["exact", "gte", "lte"],
            "profile": ["exact"],
        }
        exclude = ["id", "created_at", "updated_at"]


class StatFilter(django_filters.FilterSet):
    """
    Filter for Stat model.
    """

    class Meta:
        model = Stat
        fields = {
            "profile": ["exact"],
            "total_records": ["exact", "gte", "lte"],
            "total_exercises": ["exact", "gte", "lte"],
            "total_friends": ["exact", "gte", "lte"],
            "evaluation": ["exact", "gte", "lte"],
        }
        exclude = ["id", "created_at", "updated_at"]
