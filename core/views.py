from django.views.generic import TemplateView
from apis.models import Workout

# from django


class ProfileView(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["profile"] = self.request.user.profile
        context["workouts"] = Workout.get_profile_workouts(self.request.user.profile)
        print("Workouts: ", context["workouts"])

        return context


# def handler404(request, *args, **argv):
#     # response = render_to_response("404.html", {}, context_instance=RequestContext(request))
#     # response.status_code = 404
#     # return response
#     return redirect("admin:index")
