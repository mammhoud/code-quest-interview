# models.py

from django.db import models
from django.core.cache import cache
import pprint


class WorkoutManager(models.Manager):
    def get_queryset(self):
        try:
            cache_key = "workouts"
            workouts = cache.get(cache_key)
            if workouts is None:
                qs = super().get_queryset().annotate(total_exercises=models.Count("exercises"))
                for obj in qs.values():
                    pprint.pprint(obj, indent=4)
                print("❗ Cache miss: querying database")
                # cache the result for 10 minutes
                cache.set(cache_key, qs, timeout=30 * 1)  # 10 minutes
                return qs
            else:
                print("✔️ Cache hit -> data get from cache")
                # if the cache is not empty, we need to return the cached data
                # but we need to make sure that the data is not stale/invalid
                # so we need to check if the data is still valid
                # if the data is stale, we need to update the cache
                # and return the new data
                # we knowing if the data is stale by checking the last updated time from cached key workouts_last_updat
                # and it changed (workouts_last_update) when we update the data in the database using signal (post_save, pre_save, post_update)

                qs = workouts
                for obj in qs.values():
                    pprint.pprint(obj, indent=4)

                return qs
        except Exception as e:
            print(f": {e}")
            return super().get_queryset()

    def get_type(self, workout_type):
        """
        Filters workouts by type using cached queryset if available.
        Avoids hitting the database again if data is already cached.
        """

        # Get the full queryset (from cache if available)
        workouts = self.get_queryset()

        # Make sure we’re filtering from real objects, not just .values() dicts
        if isinstance(workouts, models.QuerySet):
            filtered = workouts.filter(workout_type=workout_type)
        else:
            # If somehow raw data (e.g., list of dicts) ends up in cache, fallback to Python filtering
            filtered = [w for w in workouts if w.get("workout_type") == workout_type]

        return filtered
        
class ExerciseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("workout")

    def get_by_workout(self, workout_id):
        cache_key = f"exercises_workout_{workout_id}"
        exercises = cache.get(cache_key)
        
        if exercises is None:
            print("❗ Cache miss: querying database")
            exercises = self.get_queryset().filter(workouts__id=workout_id)
            cache.set(cache_key, exercises, timeout=60 * 10)
        else:
            print("✔️ Cache hit -> data get from cache")
        return exercises

    def get_by_profile(self, profile_id):
        cache_key = f"exercises_profile_{profile_id}"
        exercises = cache.get(cache_key)

        if exercises is None:
            print("❗ Cache miss: querying database")
            exercises = self.get_queryset().filter(profiles__id=profile_id)
            cache.set(cache_key, exercises, timeout=60 * 10)
        else:
            print("✔️ Cache hit -> data get from cache")
        return exercises


