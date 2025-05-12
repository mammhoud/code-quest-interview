from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    Exercise,
    # Evaluation,
    # ExerciseAttendance,
    # Friend,
    # Record,
    Stat,
    Workout,
)


@admin.register(
    Exercise
)  # as same as django admin regisration but changed the class that was inherited from with the one that at django unfold
class ExerciseAdmin(ModelAdmin):
    list_display = ("name", "duration")
    search_fields = ("name",)



@admin.register(Stat)
class StatsAdmin(ModelAdmin):
    list_display = ("profile", "total_records", "total_exercises", "total_friends", "evaluation")
    search_fields = ("profile__full_name",)
    list_filter = ("evaluation",)


@admin.register(Workout)
class WorkoutAdmin(ModelAdmin):
    list_display = ("title", "date")
    search_fields = ("title",)
    list_filter = ("date",)




# @admin.register(Evaluation)
# class EvaluationAdmin(ModelAdmin):
#     list_display = ("profile", "date", "score")
#     search_fields = ("profile__full_name", "score")
#     list_filter = ("date",)


# @admin.register(ExerciseAttendance)
# class ExerciseAttendanceAdmin(ModelAdmin):
#     list_display = ("profile", "exercise", "scheduled_date", "attended")
#     search_fields = ("profile__full_name", "exercise__name")
#     list_filter = ("attended", "scheduled_date")


# @admin.register(Friend)
# class FriendAdmin(ModelAdmin):
#     list_display = ("profile", "friend", "created_at")
#     search_fields = ("profile__full_name", "friend__full_name")
#     list_filter = ("created_at",)


# @admin.register(Record)
# class RecordAdmin(ModelAdmin):
#     list_display = ("profile", "exercise", "date", "performance")
#     search_fields = ("profile__full_name", "exercise__name", "performance")
#     list_filter = ("date",)
