from apis import apiLogger
from ninja import constants
from ninja_extra import (
    ControllerBase,
    api_controller,
    route,
)
from core.exceptions import Error
from ..payload import auth_user
from ..models.schemas import UserSchema


@api_controller("", tags=["User & Profile"], auth=constants.NOT_SET, permissions=[])
class UserProfileController(ControllerBase):
    @route.get("/login", response={200: UserSchema, 404: Error})
    def Login(self, username: str, password: str):
        """
        Endpoint to list tokens for a user, including the parent token and its children.
        """
        user = auth_user(username=username, password=password, request=self.context.request)
        # self.context.route_kwargs["User-Authed"] = "true"
        # self.context.response.headers["X-User-Authed"] = "true"
        if user:
            self.context.response.headers["X-User-Authed"] = "TRUE"
            return user
        else:
            self.context.response.headers["X-User-Authed"] = "FALSE"
            return 404, {"message": "User not found."}


    