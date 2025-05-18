from typing import Optional
from django.utils.timezone import datetime
from datetime import date
from ninja import Schema, FilterSchema


# Output schema for Workout
class Workout(Schema):
    id: int
    title: str
    date: datetime
    notes: Optional[str] = None
    workout_type: str
    total_exercises: Optional[int] = 0  # Only populated via annotated queryset (e.g. in get_profile_workouts)


# Patch schema for updating Workout
class PatchWorkout(Schema):
    title: Optional[str]
    date: Optional[date]
    notes: Optional[str]
    workout_type: Optional[str]


# Filter schema for Workout
class _WorkoutFilter(FilterSchema):
    title: Optional[str] | None = None
    workout_type: Optional[str] | None = None
    date: Optional[datetime] | None = None  # type: ignore

    def filter(self, queryset):
        if self.title:
            queryset = queryset.filter(title__icontains=self.title)
        if self.workout_type:
            queryset = queryset.filter(workout_type=self.workout_type)
        if self.date:
            queryset = queryset.filter(date=self.date)
        return queryset
