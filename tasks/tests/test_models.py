import pytest
from tasks.models import Task, Status
from django.contrib.auth import get_user_model
from datetime import date, timedelta

from tasks.tests.static import USER

User = get_user_model()


@pytest.mark.django_db
def test_str_method():
    user = User.objects.create_user(username=USER["name"], password=USER["password"])
    task = Task.objects.create(
        user=user,
        title="Finish draft",
        description="Methods section",
        status=Status.PENDING,
        due_date=date.today() + timedelta(days=1),
    )
    assert str(task) == f"{task.title} - {user}"
