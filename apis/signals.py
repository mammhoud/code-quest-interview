from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db import models
from django.core.cache import cache
from .models import Exercise, Stat, Workout


@receiver([post_save, post_delete, pre_save], sender=Exercise)
def invalidate_exercise_cache(sender, instance, **kwargs):
    """
    Invalidate exercise list caches when a exercise is created, updated, or deleted
    """
    print("Clearing exercise cache")

    # Clear exercise list caches
    cache.delete_pattern("*exercises*")


@receiver([post_save, post_delete, pre_save], sender=Stat)
def invalidate_stat_cache(sender, instance, **kwargs):
    """
    Invalidate stat list caches when a stat is created, updated, or deleted
    """
    print("Clearing stat cache")

    # Clear stat list caches
    cache.delete_pattern("*stat_list*")


@receiver([post_save, post_delete, pre_save], sender=Workout)
def invalidate_workout_cache(sender, instance, **kwargs):
    """
    Invalidate workout list caches when a workout is created, updated, or deleted
    """
    print("Clearing workout cache")

    # Clear workout list caches
    cache.delete_pattern("*workouts*")
