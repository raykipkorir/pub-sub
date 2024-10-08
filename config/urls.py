from django.contrib import admin
from django.urls import path

from app.views import index, publish

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("publish/", publish),
]
