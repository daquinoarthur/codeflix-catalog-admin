import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserCanCreateAndEditCategory:
    @pytest.fixture
    def client(self):
        return APIClient()

    def test_user_can_create_and_edit_category(self, client):
        # Assert that list is emtpy
        list_response = client.get("/api/categories/")
        assert list_response.data == {
            "data": [],
            "meta": {
                "current_page": 1,
                "page_size": 2,
                "total_items": 0,
                "total_pages": 0,
            },
        }
        # Assert that the use can create a category
        create_response = client.post(
            "/api/categories/",
            data={
                "name": "Movie",
                "description": "Movie description",
            },
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_category_id = create_response.data["data"]["id"]
        assert create_response.data == {
            "data": {
                "id": created_category_id,
                "name": "Movie",
                "description": "Movie description",
                "is_active": True,
            }
        }
        # Assert that the created category is in the list
        list_response = client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                }
            ],
            "meta": {
                "current_page": 1,
                "page_size": 2,
                "total_items": 1,
                "total_pages": 1,
            },
        }
        assert len(list_response.data["data"]) == 1
        # Assert that the user can edit the category
        edit_response = client.put(
            f"/api/categories/{created_category_id}/",
            data={
                "name": "Movie updated",
                "description": "Movie description updated",
            },
            format="json",
        )
        assert edit_response.data == {
            "data": {
                "id": created_category_id,
                "name": "Movie updated",
                "description": "Movie description updated",
                "is_active": True,
            }
        }
        assert edit_response.status_code == status.HTTP_200_OK
        # Assert that the edited category is in the list
        list_response = client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie updated",
                    "description": "Movie description updated",
                    "is_active": True,
                }
            ],
            "meta": {
                "current_page": 1,
                "page_size": 2,
                "total_items": 1,
                "total_pages": 1,
            },
        }
