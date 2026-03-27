from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("drf_pyseto.urls")),
    path("", include("example_api.urls")),
]
