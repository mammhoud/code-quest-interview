from typing import List
from django.shortcuts import get_object_or_404
from ninja import Query, PatchDict
from ninja_extra import ControllerBase, api_controller, route

from core.throttle import BurstRateThrottle
from core.authentications.ninja import GlobalAuth
from core.exceptions import Error

from ..models.stats import Stat as StatModel
from ..models.schemas.stats import Stat, PatchStat, _StatFilter


@api_controller("stat/", auth=GlobalAuth(), tags=["Stat"], throttle=[BurstRateThrottle()])
class StatController(ControllerBase):
    @route.get("/list", response={200: List[Stat], 404: Error})
    def list_stats(self, filters: _StatFilter = Query(None)):
        """
        Get list of stats with optional filtering.
        """
        queryset = StatModel.objects.select_related("profile").all()
        if filters:
            queryset = filters.filter(queryset)
        return list(queryset)

    @route.get("/get/{stat_id}", response={200: Stat, 404: Error})
    def get_stat(self, request, stat_id: int):
        """
        Get a stat by ID.
        """
        stat = get_object_or_404(StatModel, id=stat_id)
        return stat

    # @route.post("/create", response={201: Stat})
    # def create_stat(self, request, payload: PatchDict[PatchStat]):
    #     """
    #     Create a new stat entry.
    #     """
    #     stat = StatModel()
    #     for attr, value in payload.items():
    #         setattr(stat, attr, value)
    #     stat.save()
    #     return 201, stat

    @route.patch("/update/{stat_id}", response={200: Stat})
    def update_stat(self, request, stat_id: int, payload: PatchDict[PatchStat]):
        """
        Update an existing stat.
        """
        stat = get_object_or_404(StatModel, id=stat_id)
        for attr, value in payload.items():
            setattr(stat, attr, value)
        stat.save()
        return stat

    @route.delete("/delete/{stat_id}", response={204: None})
    def delete_stat(self, request, stat_id: int):
        """
        Delete a stat entry.
        """
        stat = get_object_or_404(StatModel, id=stat_id)
        stat.delete()
        return 204, None

    @route.get("/get/{profile_id}", response={200: Stat, 404: Error})
    def get_profile_stat(self, request, profile_id: int):
        stat = StatModel.objects.get_by_profile(profile_id=profile_id)
        if stat:
            return 200, stat
        else:
            return 404, {"message": "profile not stored with stat"}
