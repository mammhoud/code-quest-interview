from django.urls import path
# from apis.views import *

from ninja_extra import NinjaExtraAPI
from ninja import Swagger
from .controllers import *

api = NinjaExtraAPI(
    title="SWAGGER API",
    version="0.1.beta",
    description="A simple API for workout & exercise tracking",
    openapi_url="/openapi.json",
    docs=Swagger(),
    docs_url="/docs",
    urls_namespace="APIS",
    auth=NOT_SET,
    app_name="APIS",
    csrf=True,
    # docs_decorator: (TCallable) -> TCallable | None = None,
    # servers: list[dict[str, Any]] | None = None,
    # renderer: BaseRenderer | None = None,
    # parser: Parser | None = None,
    # openapi_extra: dict[str, Any] | None = None,
)
api.auto_discover_controllers()
# urlpatterns = [
#     path("stats/", StatListCreateView.as_view(), name="stats-list-create"),
#     path("workouts/", WorkoutListCreateView.as_view(), name="workouts-list-create"),
#     path("exercises/", ExerciseListCreateView.as_view(), name="exercises-list-create"),
# ]
# urlpatterns += [
#     path("stats/<int:pk>/", StatRetrieveUpdateDestroyView.as_view(), name="stats-detail"),
#     path("workouts/<int:pk>/", WorkoutRetrieveUpdateDestroyView.as_view(), name="workouts-detail"),
#     path("exercises/<int:pk>/", ExerciseRetrieveUpdateDestroyView.as_view(), name="exercises-detail"),
# ]


urlpatterns = [
    path("", api.urls),
]
