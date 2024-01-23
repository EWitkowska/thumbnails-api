"""
URL configuration for thumbnails_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from users.urls import router as users_router
from thumbnails.urls import (
    router as thumbnails_router,
)

main_router = DefaultRouter()
main_router.registry.extend(users_router.registry)
main_router.registry.extend(thumbnails_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="api/v1/")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/", include(main_router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
