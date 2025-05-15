from typing import Optional, List
from datetime import datetime
from ninja import Schema, FilterSchema


# Minimal Profile schema for reference in Exercise
class _Profile(Schema):
    id: int
    full_name: Optional[str] = None


# Minimal Workout schema for reference in Exercise
class _Workout(Schema):
    id: int
    title: str  # assuming Workout has a 'name' field


# Schema for full Exercise detail (used for API responses)
class Exercise(Schema):
    id: int
    name: str
    description: Optional[str] = None
    duration: Optional[int]
    profile: _Profile
    workouts: List[_Workout]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    # total_exercises: Optional[int] = None  # for aggregation purposes


# Patch schema for partial update
class PatchExercise(Schema):
    name: Optional[str]
    description: Optional[str]
    duration: Optional[int]
    profile_id: Optional[int]
    # workouts_ids: Optional[List[int]]  # You may handle this explicitly in views @ TODO add a schema for post with workouts dict insertions
    # created_at 
    # & updated_at not patchable


# Filter schema for Exercise model
class _ExerciseFilter(FilterSchema):
    full_name: Optional[str] | None = None
    duration: Optional[int] | None = None
    profile_id: Optional[int] | None = None

    def filter(self, queryset):
        if self.duration is not None:
            queryset = queryset.filter(duration=self.duration)
        if self.profile_id:
            queryset = queryset.filter(profile_id=self.profile_id)
        if self.full_name:
            queryset = queryset.filter(profile__full_name__icontains=self.full_name)
        return queryset
