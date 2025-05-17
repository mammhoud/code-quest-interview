from ninja_extra import permissions
from ninja_extra import api_controller, http_get, ControllerBase
from django.http import HttpRequest
from core import coreLogger as logger


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, controller: ControllerBase):
        # Access route context and compute parameters
        controller.context.compute_route_parameters()

        # Now you can access path and query parameters
        user = request.user
        user_id = user.id

        if request.token.profile.user.is_superuser:
            return True
        if user_id == request.user.id:
            return True

        # todo: user data with perm caches
