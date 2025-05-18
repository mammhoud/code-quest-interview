from apis import apiLogger
from ninja import constants
from ninja_extra import ControllerBase, api_controller, route, permissions
from core.exceptions import Error
from core.permissions.ninja import IsOwnerOrReadOnly
from ..payload import auth_user
from ..models.schemas import Profile as ProfileSchema
from ninja.files import UploadedFile
from ninja import File
from core.authentications.ninja import GlobalAuth


@api_controller("/profile", tags=["User & Profile"], auth=GlobalAuth())
class UserProfileController(ControllerBase):
    @route.put("/login", response={200: ProfileSchema, 404: Error}, permissions=[IsOwnerOrReadOnly()])
    def Login(self, username: str, password: str):
        """
        Endpoint to list tokens for a user, including the parent token and its children.
        """
        user = auth_user(username=username, password=password, request=self.context.request)
        self.context.user = user

        if user:
            self.context.response.headers["X-USER-AUTH"] = "True"
            self.context.response.headers["X-USER-ID"] = user.id
            return 200, user.profile
        else:
            self.context.response.headers["X-User-Authed"] = "False"
            return 404, {"message": "User not found."}

    @route.post(
        "/profileImage",
    )
    def update_ProfilImage(self, file: UploadedFile = File(...)):  # noqa: B008
        # url_file = file_upload(file)
        # apiLogger.info(f"url_file {url_file}")
        if self.context.request:
            profile = self.context.request.profile
            profile.profile_image.save(file.name, file)
            profile.save()
        return {"name": profile.profile_image.url}


# def file_upload(file):
#     from django.core.files.storage import FileSystemStorage
#     fs = FileSystemStorage()
#     filename = fs.save(, file)
#     uploaded_file_url = fs.url(filename)
#     return uploaded_file_url
