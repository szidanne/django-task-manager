from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner


@extend_schema_view(
    list=extend_schema(
        tags=["tasks"],
        summary="List my tasks",
        description="Returns tasks owned by the authenticated user.",
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search title/description",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="ordering",
                description="Order by: due_date, -created_at, status, title",
                required=False,
                type=str,
            ),
        ],
    ),
    retrieve=extend_schema(tags=["tasks"], summary="Get a task"),
    create=extend_schema(tags=["tasks"], summary="Create a task"),
    update=extend_schema(tags=["tasks"], summary="Replace a task"),
    partial_update=extend_schema(tags=["tasks"], summary="Update part of a task"),
    destroy=extend_schema(tags=["tasks"], summary="Delete a task"),
)
class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD for the authenticated user's tasks.
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    # Per-user scoping
    def get_queryset(self):
        # Supports ?search=, ?ordering=, etc. via DRF filters (see settings)
        return Task.objects.filter(user=self.request.user).order_by(
            "status", "due_date", "-created_at"
        )

    # Auto-assign owner on create
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Prevent changing owner via update
    def perform_update(self, serializer):
        if "user" in serializer.validated_data:
            raise PermissionDenied("Cannot change owner of a task.")
        serializer.save()

    # Extra: default ordering and searchable fields
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "created_at", "updated_at", "status", "title"]
