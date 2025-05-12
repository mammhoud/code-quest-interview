from django.urls import path
from apis.views import StatsListCreateView


urlpatterns = [
   path("stats/", StatsListCreateView.as_view(), name="stats-list-create"),
]
