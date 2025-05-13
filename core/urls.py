from django.contrib import admin  # Noqa
from django.urls import path, include  # Noqa

# from django.template.response import TemplateResponse  # Noqa
from .views import ProfileView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from graphene_django.views import GraphQLView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/", include("apis.routers")),
        path("api-auth/", include("rest_framework.urls")),
        path("accounts/profile/", ProfileView.as_view(), name="account_profile"),
        path("graphql", GraphQLView.as_view(graphiql=True)),
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        # Optional UI:
        # path("api/docs-r/", SpectacularRedocView.as_view(url_name="schema-file"), name="redoc"),
        path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
