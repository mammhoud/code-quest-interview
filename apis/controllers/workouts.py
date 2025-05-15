from typing import List

from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import PatchDict, Query
from ninja.constants import NOT_SET
from ninja_extra import ControllerBase, api_controller, route, status
from ninja import Form
from ..models.workouts import Workout as workoutModel
from ..models.schemas.workouts import *
from ..models.schemas.workouts import _WorkoutFilter
# from core.base.io.exceptions import *


@api_controller("workouts/", auth=NOT_SET, tags=["Workout"], permissions=[])
class WorkoutController(ControllerBase):
    @route.get("/list", response={200: List[Workout]}, permissions=[])  # noqa: UP006
    def get_workouts(self, filters: _WorkoutFilter = Query(None)):  # noqa: B008
        """
        Get a list of workouts with optional filtering.
        """
        queryset = workoutModel.objects.all()
        if filters:
            # queryset = queryset.filter(**filters)
            queryset = filters.filter(queryset) if filters else queryset
        return list(queryset)
