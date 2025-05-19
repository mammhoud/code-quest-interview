from django.utils.timezone import datetime

from ninja import FilterSchema, Schema


from .user import UserSchema as _User

# Profile schema for API responses
class PatchProfile(Schema):
    # id: int
    user_id: int | None
    bio: str | None
    birth_date: datetime | None
    created_at: datetime | None
    full_name: str | None
    profile_image: str | None
    cover_image: str | None
    language: str
    notes: str | None


# Profile schema for API responses
class Profile(Schema):
    id: int
    user: _User
    bio: str | None
    birth_date: datetime | None
    created_at: datetime | None
    full_name: str | None
    profile_image: str | None
    cover_image: str | None
    language: str
    notes: str | None


# Filter schema for Profile model
class _ProfileFilter(FilterSchema):
    full_name: str | None
    birth_date: datetime | None
    bio: str | None
    language: str | None

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
