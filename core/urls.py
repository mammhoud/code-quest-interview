from django.contrib import admin  # Noqa
from django.urls import path, include  # Noqa

# from django.template.response import TemplateResponse  # Noqa
from .views import ProfileView
from django.conf.urls.static import static
from django.conf import settings

from graphene_django.views import GraphQLView

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/v1/", include("apis.routers")),
        path("api-auth/", include("rest_framework.urls")),
        path("accounts/profile/", ProfileView.as_view(), name="account_profile"),
        path("graphql", GraphQLView.as_view(graphiql=True)),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
