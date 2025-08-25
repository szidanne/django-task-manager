import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from tasks.models import Task, Status
from datetime import date, timedelta

from tasks.tests.static import USER, OTHER_USER

User = get_user_model()

LIST_URL = lambda: reverse("tasks:task-list")
DETAIL_URL = lambda pk: reverse("tasks:task-detail", args=[pk])


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username=USER["name"], password=USER["password"])


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client, user


def _items(data):
    """Return list items whether pagination is enabled or not."""
    return data["results"] if isinstance(data, dict) and "results" in data else data


@pytest.mark.django_db
def test_list_returns_only_my_tasks(auth_client):
    client, user = auth_client
    my_task = Task.objects.create(
        user=user,
        title="Mine",
        description="",
        status=Status.PENDING,
        due_date=date.today(),
    )
    other = User.objects.create_user(
        username=OTHER_USER["name"], password=OTHER_USER["password"]
    )
    Task.objects.create(
        user=other,
        title="Not mine",
        description="",
        status=Status.PENDING,
        due_date=date.today(),
    )

    res = client.get(LIST_URL())
    assert res.status_code == 200
    items = _items(res.data)
    ids = [item["id"] for item in items]
    assert ids == [my_task.id]  # only Alice's task returned


@pytest.mark.django_db
def test_create_task_sets_owner(auth_client):
    client, user = auth_client
    payload = {
        "title": "New",
        "description": "desc",
        "status": Status.PENDING,
        "due_date": (date.today() + timedelta(days=2)).isoformat(),
    }
    res = client.post(LIST_URL(), payload, format="json")
    assert res.status_code == 201
    assert Task.objects.get(id=res.data["id"]).user == user
