from django.contrib import admin
from unfold.admin import ModelAdmin


from .models import (
    Profile,
)


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("user", "full_name", "language")
    search_fields = ("user__username", "bio", "language", "full_name")
    list_filter = ("birth_date",)
    ordering = ("user__username", "full_name")
    list_per_page = 20
    list_select_related = ("user",)
    list_editable = ("full_name", "language")
    list_display_links = ("user",)
