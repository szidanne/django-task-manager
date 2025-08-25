from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.routers import DefaultRouter

from . import views
from .api import TaskViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

app_name = "tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:task_id>/", views.detail, name="detail"),
    path("new/", views.create_task, name="create"),
    path("<int:task_id>/edit/", views.edit_task, name="edit"),
    path("<int:task_id>/delete/", views.delete_task, name="delete"),
    # rest api
    path("api/", include(router.urls)),
    # OpenAPI schema & UIs, namespaced to this app
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="tasks:schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="tasks:schema"),
        name="redoc",
    ),
]
