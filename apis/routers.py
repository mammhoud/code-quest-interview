from django.urls import path
from apis.views import *

urlpatterns = [
    path("stats/", StatListCreateView.as_view(), name="stats-list-create"),
    path("workouts/", WorkoutListCreateView.as_view(), name="workouts-list-create"),
    path("exercises/", ExerciseListCreateView.as_view(), name="exercises-list-create"),
]
urlpatterns += [
    path("stats/<int:pk>/", StatRetrieveUpdateDestroyView.as_view(), name="stats-detail"),
    path("workouts/<int:pk>/", WorkoutRetrieveUpdateDestroyView.as_view(), name="workouts-detail"),
    path("exercises/<int:pk>/", ExerciseRetrieveUpdateDestroyView.as_view(), name="exercises-detail"),
]
