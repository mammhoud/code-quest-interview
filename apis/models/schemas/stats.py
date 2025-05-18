from typing import Optional
from datetime import datetime
from ninja import Schema, FilterSchema


# Minimal Profile schema for relation
class _Profile(Schema):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]


# Full schema for returning Stat data
class Stat(Schema):
    id: int
    profile: Optional[_Profile]
    total_exercises: int
    total_workouts: int
    evaluation: int
    created_at: datetime
    updated_at: datetime


# Patch schema for partial updates
class PatchStat(Schema):
    profile_id: Optional[int]
    total_exercises: Optional[int]
    total_workouts: Optional[int]
    evaluation: Optional[int]


# Filter schema for querying Stat records
class _StatFilter(FilterSchema):
    profile_id: Optional[int]
    evaluation: Optional[int]

    def filter(self, queryset):
        if self.profile_id:
            queryset = queryset.filter(profile_id=self.profile_id)
        if self.evaluation is not None:
            queryset = queryset.filter(evaluation=self.evaluation)
        return queryset
