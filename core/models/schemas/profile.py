from django.utils.timezone import datetime
from typing import Optional

from ninja import FilterSchema, Schema


from .user import UserSchema as _User

# Profile schema for API responses
class PatchProfile(Schema):
    # id: int
    user_id: Optional[int]
    bio: Optional[str]
    birth_date: Optional[datetime]
    created_at: Optional[datetime]
    full_name: Optional[str]
    profile_image: Optional[str]
    cover_image: Optional[str]
    language: str
    notes: Optional[str]


# Profile schema for API responses
class Profile(Schema):
    id: int
    user: _User
    bio: Optional[str]
    birth_date: Optional[datetime]
    created_at: Optional[datetime]
    full_name: Optional[str]
    profile_image: Optional[str]
    cover_image: Optional[str]
    language: str
    notes: Optional[str]


# Filter schema for Profile model
class _ProfileFilter(FilterSchema):
    full_name: Optional[str]
    birth_date: Optional[datetime]
    bio: Optional[str]
    language: Optional[str]

    def filter(self, queryset):
        """
        Applies filters to the given queryset.
        """
        if self.full_name:
            queryset = queryset.filter(full_name__icontains=self.full_name)
        if self.birth_date:
            queryset = queryset.filter(birth_date=self.birth_date)
        if self.bio is not None:
            queryset = queryset.filter(bio__icontains=self.bio)
        if self.language:
            queryset = queryset.filter(language__icontains=self.language)
        return queryset
