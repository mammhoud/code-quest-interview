from django.contrib import admin  # Noqa
from django.urls import path, include  # Noqa

# from django.template.response import TemplateResponse  # Noqa
from .views import ProfileView
from django.conf.urls.static import static
from django.conf import settings
from graphene_django.views import GraphQLView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from apis.routers import ninja_apis as ninja_apis

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("apis.routers"), name="apis"),
        # path("api-auth/", include("rest_framework.urls")),
        path("accounts/profile/", ProfileView.as_view(), name="account_profile"),
        path("graphql", GraphQLView.as_view(graphiql=True)),
        path("api/schema/", SpectacularAPIView.as_view(), name="schema-file"),
        # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        # Optional UI:
        path("docs/redoc", SpectacularRedocView.as_view(url_name="schema-file"), name="redoc"),
        # path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema-file"), name="swagger-ui"),
        ################
        path("", ninja_apis.urls),
        # path("",handler404)
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if "debug_toolbar" in settings.INSTALLED_APPS:
    from src.settings.debug_toolbar.setup import DebugToolbarSetup  # noqa

    urlpatterns = DebugToolbarSetup.do_urls(urlpatterns)


handler404 = "core.views.handler404"
handler500 = "core.views.handler404"
