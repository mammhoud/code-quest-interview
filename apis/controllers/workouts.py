from django.shortcuts import get_object_or_404
from ninja import Query, PatchDict
from ninja_extra import ControllerBase, api_controller, route

from core.throttle import BurstRateThrottle
from core.exceptions import Error
from core.authentications.ninja import GlobalAuth

from ..models.workouts import Workout as WorkoutModel
from ..models.schemas.workouts import Workout, PatchWorkout, _WorkoutFilter


@api_controller("workout/", auth=GlobalAuth(), tags=["Workout"], permissions=[])
class WorkoutController(ControllerBase):
    @route.get("/list", response={200: list[Workout], 404: Error}, throttle=[BurstRateThrottle()])
    def list_workouts(self, filters: _WorkoutFilter = Query(None)):  # noqa: B008
        """
        Get a list of workouts with optional filtering.
        """
        queryset = WorkoutModel.objects.all()
        if filters:
            queryset = filters.filter(queryset)
        return list(queryset)

    @route.put("/bulk", response={200: list[Workout]}, permissions=[])  # noqa: UP006
    def bulk_create_workouts(self, request, payload: list[PatchDict[PatchWorkout]]):  # noqa: B008, UP006
        """
        bulk Creation of workoutss.
        """
        workouts = []
        for item in payload:
            workouts = WorkoutModel()
            for attr, value in item.items():
                setattr(workouts, attr, value)
            workouts.save()
            workouts.append(workouts)
        return workouts

    @route.get("/get_type/{workout_type}", response={200: Workout, 404: Error})
    def get_workout_bytype(self, request, workout_type: str):
        """
        Get a workout by ID.
        """
        workout = WorkoutModel.objects.get_type(workout_type=workout_type)
        return workout

    @route.get("/get/{workout_id}", response={200: Workout, 404: Error})
    def get_workout(self, request, workout_id: int):
        """
        Get a workout by ID.
        """
        workout = get_object_or_404(WorkoutModel, id=workout_id)
        return workout

    @route.post("/create", response={201: Workout})
    def create_workout(self, request, payload: PatchDict[PatchWorkout]):
        """
        Create a new workout.
        """
        workout = WorkoutModel()
        for attr, value in payload.items():
            setattr(workout, attr, value)
        workout.save()
        return 201, workout

    @route.patch("/update/{workout_id}", response={200: Workout})
    def update_workout(self, request, workout_id: int, payload: PatchDict[PatchWorkout]):
        """
        Update an existing workout.
        """
        workout = get_object_or_404(WorkoutModel, id=workout_id)
        for attr, value in payload.items():
            setattr(workout, attr, value)
        workout.save()
        return workout

    @route.delete("/delete/{workout_id}", response={204: None})
    def delete_workout(self, request, workout_id: int):
        """
        Delete a workout by ID.
        """
        workout = get_object_or_404(WorkoutModel, id=workout_id)
        workout.delete()
        return 204, None
