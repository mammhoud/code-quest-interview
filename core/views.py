from django.views.generic import TemplateView
import pprint
from apis.models import Workout
class ProfileView(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["profile"] = self.request.user.profile
        context["workouts"] = Workout.get_profile_workouts(self.request.user.profile)
        print("Workouts: ", context["workouts"])
        
        return context
