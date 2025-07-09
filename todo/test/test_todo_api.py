import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User
from todo.models import Task


# Fixtures for creating test data
@pytest.fixture
def user():
    return User.objects.create_user(
        email="mirfallahi2009@gmail.com", password="testpass"
    )


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.mark.django_db
class TestTodoAPI:
    def test_get_tasks_response_200(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("todo:task-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_task_response_201(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("todo:task-list")
        data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "completed": False,
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == 1
        assert Task.objects.get().title == "Test Task"

    def test_update_task_response_200(self, api_client, user):
        api_client.force_authenticate(user=user)
        task = Task.objects.create(
            title="Old Task",
            description="This is an old task.",
            status=False,
            user=user,
        )
        url = reverse("todo:task-detail", kwargs={"pk": task.pk})
        data = {
            "title": "Updated Task",
            "description": "This is an updated task.",
            "status": True,
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.title == "Updated Task"
        assert task.status is True

    def test_delete_task_response_204(self, api_client, user):
        api_client.force_authenticate(user=user)
        task = Task.objects.create(
            title="Task to be deleted",
            description="This task will be deleted.",
            status=False,
            user=user,
        )
        url = reverse("todo:task-detail", kwargs={"pk": task.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.count() == 0

    def test_get_task_detail_response_200(self, api_client, user):
        api_client.force_authenticate(user=user)
        task = Task.objects.create(
            title="Detail Task",
            description="This is a detail task.",
            status=False,
            user=user,
        )
        url = reverse("todo:task-detail", kwargs={"pk": task.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Detail Task"
        assert response.data["description"] == "This is a detail task."
        assert response.data["status"] is False

    def test_get_task_detail_not_found(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse(
            "todo:task-detail", kwargs={"pk": 999}
        )  # Assuming this ID does not exist
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_task_unauthenticated(self, api_client, user):
        url = reverse("todo:task-list")
        data = {
            "title": "Unauthenticated Task",
            "description": "This task should not be created.",
            "status": False,
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Task.objects.count() == 0

    def test_update_task_unauthenticated(self, api_client, user):
        task = Task.objects.create(
            title="Unauthenticated Update Task",
            description="This task should not be updated.",
            status=False,
            user=user,
        )
        url = reverse("todo:task-detail", kwargs={"pk": task.pk})
        data = {
            "title": "Updated Task",
            "description": "This is an updated task.",
            "status": True,
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        task.refresh_from_db()
        assert task.title == "Unauthenticated Update Task"

    def test_delete_task_unauthenticated(self, api_client, user):
        task = Task.objects.create(
            title="Unauthenticated Delete Task",
            description="This task should not be deleted.",
            status=False,
            user=user,
        )
        url = reverse("todo:task-detail", kwargs={"pk": task.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Task.objects.count() == 1

    def test_get_tasks_unauthenticated(self, api_client):
        url = reverse("todo:task-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_toggle_task_status_response_200(self, api_client, user):
        api_client.force_authenticate(user=user)
        task = Task.objects.create(
            title="Toggle Task",
            description="This task will have its status toggled.",
            status=False,
            user=user,
        )
        url = reverse("todo:task-toggle-status", kwargs={"pk": task.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.status is True
        assert response.data["status"] is True
