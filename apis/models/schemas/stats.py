from django.utils.timezone import datetime
from ninja import Schema, FilterSchema


# Minimal Profile schema for relation
class _Profile(Schema):
    id: int
    first_name: str | None
    last_name: str | None


# Full schema for returning Stat data
class Stat(Schema):
    id: int
    profile: _Profile | None
    total_exercises: int
    total_workouts: int
    evaluation: int
    created_at: datetime
    updated_at: datetime


# Patch schema for partial updates
class PatchStat(Schema):
    profile_id: int | None
    total_exercises: int | None
    total_workouts: int | None
    evaluation: int | None


# Filter schema for querying Stat records
class _StatFilter(FilterSchema):
    profile_id: int | None
    evaluation: int | None

    def filter(self, queryset):
        if self.profile_id:
            queryset = queryset.filter(profile_id=self.profile_id)
        if self.evaluation is not None:
            queryset = queryset.filter(evaluation=self.evaluation)
        return queryset
