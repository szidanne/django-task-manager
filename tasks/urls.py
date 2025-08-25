from django.urls import path

from . import views

app_name = "tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:task_id>/", views.detail, name="detail"),
    path("new/", views.create_task, name="create"),
    path("<int:task_id>/edit/", views.edit_task, name="edit"),
    path("<int:task_id>/delete/", views.delete_task, name="delete"),
]
