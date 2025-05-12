"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

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
