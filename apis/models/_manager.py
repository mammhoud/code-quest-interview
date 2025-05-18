# models.py

from django.db import models
from django.core.cache import cache
from core import coreLogger as logger


class StatManager(models.Manager):
    def get_queryset(self):
        try:
            cache_key = "stats"
            stats = cache.get(cache_key)

            if stats is None:
                logger.warning("Cache miss: querying stats from database")
                qs = super().get_queryset().select_related("profile")
                cache.set(cache_key, qs, timeout=60 * 10)
                return qs
            else:
                logger.info("Cache hit -> stats data from cache")
                return stats
        except Exception as e:
            logger.warning("Error in StatManager.get_queryset")
            return super().get_queryset()

    def get_by_profile(self, profile_id):
        try:
            cache_key = f"stat_profile_{profile_id}"
            stat = cache.get(cache_key)

            if stat is None:
                logger.warning(f"Cache miss: querying stat by profile {profile_id}")
                try:
                    stat = self.get_queryset().get(profile_id=profile_id)
                    cache.set(cache_key, stat, timeout=60 * 10)
                except self.model.DoesNotExist:
                    logger.warning(f"No stat found for profile {profile_id}")
                    return None
            else:
                logger.info(f"Cache hit for stat by profile {profile_id}")
            return stat
        except Exception as e:
            logger.warning("Error in StatManager.get_by_profile")
            return None

    def top_evaluated(self, limit=10):
        try:
            return self.get_queryset().order_by("-evaluation")[:limit]
        except Exception:
            logger.warning("Error in StatManager.top_evaluated")
            return self.none()


class WorkoutManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        try:
            cache_key = "workouts"
            workouts = cache.get(cache_key)

            if workouts is None:
                logger.warning("Cache miss: querying workouts from database")
                qs = super().get_queryset().annotate(total_exercises=models.Count("exercises"))
                cache.set(cache_key, qs, timeout=30 * 1)
                return qs
            else:
                logger.info("Cache hit -> workouts from cache")
                return workouts.to_queryset()
        except Exception:
            logger.warning("Error in WorkoutManager.get_queryset")
            return super().get_queryset()

    def get_type(self, workout_type):
        try:
            workouts = self.get_queryset()
            if isinstance(workouts, models.QuerySet):
                return workouts.filter(workout_type=workout_type)
            else:
                return [w for w in workouts if w.get("workout_type") == workout_type]
        except Exception:
            logger.warning("Error in WorkoutManager.get_type")
            return self.none()


class ExerciseManager(models.Manager):
    def get_queryset(self):
        try:
            cache_key = "exercises"
            exercises = cache.get(cache_key)

            if exercises is None:
                logger.warning("Cache miss: querying exercises from database")
                qs = super().get_queryset()
                cache.set(cache_key, qs, timeout=60 * 10)
                return qs
            else:
                logger.info("Cache hit -> exercises from cache")
                return exercises.to_queryset()
        except Exception:
            logger.warning("Error in ExerciseManager.get_queryset")
            return super().get_queryset()

    def get_by_workout(self, workout_id):
        try:
            cache_key = f"exercises_workout_{workout_id}"
            exercises = cache.get(cache_key)

            if exercises is None:
                logger.warning(f"Cache miss: querying exercises for workout {workout_id}")
                exercises = self.get_queryset().filter(workouts__id=workout_id)
                cache.set(cache_key, exercises, timeout=60 * 10)
            else:
                logger.info(f"Cache hit -> exercises for workout {workout_id}")
            return exercises
        except Exception:
            logger.warning("Error in ExerciseManager.get_by_workout")
            return self.none()

    def get_by_profile(self, profile_id):
        try:
            cache_key = f"exercises_profile_{profile_id}"
            exercises = cache.get(cache_key)

            if exercises is None:
                logger.warning(f"Cache miss: querying exercises for profile {profile_id}")
                exercises = self.get_queryset().filter(profile_id=profile_id)
                cache.set(cache_key, exercises, timeout=60 * 10)
            else:
                logger.info(f"Cache hit -> exercises for profile {profile_id}")
            return exercises
        except Exception:
            logger.warning("Error in ExerciseManager.get_by_profile")
            return self.none()
