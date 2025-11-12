from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("myblog/", include("myblog.urls")),   # ← є
]

