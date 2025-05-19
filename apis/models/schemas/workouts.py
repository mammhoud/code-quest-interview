from django.utils.timezone import datetime
from datetime import date
from ninja import Schema, FilterSchema


# Output schema for Workout
class Workout(Schema):
    id: int
    title: str
    date: datetime
    notes: str | None = None
    workout_type: str
    total_exercises: int | None = 0  # Only populated via annotated queryset (e.g. in get_profile_workouts)


# Patch schema for updating Workout
class PatchWorkout(Schema):
    title: str | None
    date: date | None
    notes: str | None
    workout_type: str | None


# Filter schema for Workout
class _WorkoutFilter(FilterSchema):
    title: str | None | None = None
    workout_type: str | None | None = None
    date: datetime | None | None = None  # type: ignore

    def filter(self, queryset):
        if self.title:
            queryset = queryset.filter(title__icontains=self.title)
        if self.workout_type:
            queryset = queryset.filter(workout_type=self.workout_type)
        if self.date:
            queryset = queryset.filter(date=self.date)
        return queryset
