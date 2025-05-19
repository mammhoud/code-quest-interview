from core import coreLogger as logger
from django.db import models
from django.core.cache import cache


class StatManager(models.Manager):
    def get_queryset(self):
        cache_key = "stats"
        stats = cache.get(cache_key)

        if stats is None:
            logger.info("❗ Cache miss: querying Stat from database")
            try:
                qs = super().get_queryset().select_related("profile")
                cache.set(cache_key, qs, timeout=60 * 10)
                return qs
            except Exception as e:
                logger.warning(f"⚠️ Warning in StatManager.get_queryset: {e}")
                return super().get_queryset()
        else:
            logger.info("✔️ Cache hit -> Stat data from cache")
            return stats

    def get_by_profile(self, profile_id):
        cache_key = f"stat_profile_{profile_id}"
        stat = cache.get(cache_key)

        if stat is None:
            logger.info(f"❗ Cache miss: querying stat for profile_id={profile_id}")
            try:
                stat = self.get_queryset().get(profile_id=profile_id)
                cache.set(cache_key, stat, timeout=60 * 10)
            except self.model.DoesNotExist:
                logger.warning(f"Stat for profile_id={profile_id} does not exist")
                return None
            except Exception as e:
                logger.warning(f"⚠️ Warning in StatManager.get_by_profile: {e}")
                return None
        else:
            logger.info("✔️ Cache hit -> stat by profile")

        return stat

    def top_evaluated(self, limit=10):
        try:
            return self.get_queryset().order_by("-evaluation")[:limit]
        except Exception as e:
            logger.warning(f"⚠️ Warning in StatManager.top_evaluated: {e}")
            return self.get_queryset().none()


class WorkoutManager(models.Manager):
    def get_queryset(self):
        cache_key = "workouts"
        workouts = cache.get(cache_key)

        if workouts is None:
            logger.info("❗ Cache miss: querying workouts")
            try:
                qs = super().get_queryset().annotate(total_exercises=models.Count("exercises"))
                cache.set(cache_key, qs, timeout=60 * 10)
                return qs
            except Exception as e:
                logger.warning(f"⚠️ Warning in WorkoutManager.get_queryset: {e}")
                return super().get_queryset()
        else:
            logger.info("✔️ Cache hit -> workouts data from cache")
            if isinstance(workouts, models.QuerySet):
                return workouts
            else:
                logger.warning("⚠️ Cached workouts is not a QuerySet. Returning as-is.")
                return workouts

    def get_type(self, workout_type):
        try:
            workouts = self.get_queryset()

            if isinstance(workouts, models.QuerySet):
                return workouts.filter(workout_type=workout_type)
            else:
                return [w for w in workouts if isinstance(w, dict) and w.get("workout_type") == workout_type]
        except Exception as e:
            logger.warning(f"⚠️ Warning in WorkoutManager.get_type: {e}")
            return []


class ExerciseManager(models.Manager):
    def get_queryset(self):
        cache_key = "exercises"
        exercises = cache.get(cache_key)

        if exercises is None:
            logger.info("❗ Cache miss: querying exercises")
            try:
                qs = super().get_queryset()
                cache.set(cache_key, qs, timeout=60 * 10)
                return qs
            except Exception as e:
                logger.warning(f"⚠️ Warning in ExerciseManager.get_queryset: {e}")
                return super().get_queryset()
        else:
            logger.info("✔️ Cache hit -> exercises data from cache")
            if isinstance(exercises, models.QuerySet):
                return exercises
            else:
                logger.warning("⚠️ Cached exercises is not a QuerySet. Returning as-is.")
                return exercises

    def get_by_workout(self, workout_id):
        cache_key = f"exercises_workout_{workout_id}"
        exercises = cache.get(cache_key)

        if exercises is None:
            logger.info(f"❗ Cache miss: querying exercises for workout_id={workout_id}")
            try:
                exercises = self.get_queryset().filter(workouts__id=workout_id)
                cache.set(cache_key, exercises, timeout=60 * 10)
            except Exception as e:
                logger.warning(f"⚠️ Warning in get_by_workout: {e}")
                return self.get_queryset().none()
        else:
            logger.info("✔️ Cache hit -> exercises by workout")
        return exercises

    def get_by_profile(self, profile_id):
        cache_key = f"exercises_profile_{profile_id}"
        exercises = cache.get(cache_key)

        if exercises is None:
            logger.info(f"❗ Cache miss: querying exercises for profile_id={profile_id}")
            try:
                exercises = self.get_queryset().filter(profile_id=profile_id)
                cache.set(cache_key, exercises, timeout=60 * 10)
            except Exception as e:
                logger.warning(f"⚠️ Warning in get_by_profile: {e}")
                return self.get_queryset().none()
        else:
            logger.info("✔️ Cache hit -> exercises by profile")
        return exercises
