import uuid

import pytest
from rest_framework import status
from rest_framework.fields import ErrorDetail
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.mark.django_db
class CommonTestFixtures:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def category_repository(self):
        return DjangoORMCategoryRepository()

    @pytest.fixture
    def create_category(self, category_repository: DjangoORMCategoryRepository):
        def _create_category(name, description):
            category = Category(
                name=name,
                description=description,
            )
            category_repository.save(category)
            return category

        return _create_category


class TestListCategoriesAPI(CommonTestFixtures):
    def test_list_categories(self, client: APIClient, create_category):
        category_movies = create_category(
            name="Movies",
            description="Movies category",
        )
        category_documentary = create_category(
            name="Documentary",
            description="Documentary category",
        )
        category_path = "/api/categories/"
        response = client.get(path=category_path)
        expected_response = {
            "data": [
                {
                    "id": str(category_documentary.id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active,
                },
                {
                    "id": str(category_movies.id),
                    "name": category_movies.name,
                    "description": category_movies.description,
                    "is_active": category_movies.is_active,
                },
            ]
        }
        assert response.data == expected_response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        category_documentary_response = response.data["data"][0]
        assert category_documentary_response["id"] == str(category_documentary.id)
        assert category_documentary_response["name"] == category_documentary.name
        assert (
            category_documentary_response["description"]
            == category_documentary.description
        )
        assert (
            category_documentary_response["is_active"] == category_documentary.is_active
        )
        category_movie_response = response.data["data"][1]
        assert category_movie_response["id"] == str(category_movies.id)
        assert category_movie_response["name"] == category_movies.name
        assert category_movie_response["description"] == category_movies.description
        assert category_movie_response["is_active"] == category_movies.is_active

    def test_list_categories_empty(self, client: APIClient):
        category_path = "/api/categories/"
        response = client.get(path=category_path)

        assert response.data == {"data": []}
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 0


class TestRetrieveCategoryAPI(CommonTestFixtures):
    def test_retrieve_category_when_id_is_not_a_valid_uuid(self, client: APIClient):
        category_path = "/api/categories/invalid-uuid/"
        response = client.get(path=category_path)

        expected_response = {
            "id": [ErrorDetail(string="Must be a valid UUID.", code="invalid")]
        }

        assert response.data == expected_response
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_category_when_exists(
        self,
        client: APIClient,
        create_category,
    ):
        category_movie = create_category(
            name="Movies",
            description="Movies category",
        )
        create_category(
            name="Documentary",
            description="Documentary category",
        )
        category_path = f"/api/categories/{category_movie.id}/"
        response = client.get(path=category_path)

        expected_response = {
            "data": {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            }
        }

        assert response.data == expected_response
        assert response.status_code == status.HTTP_200_OK

    def test_return_404_when_category_not_exists(
        self,
        client: APIClient,
        create_category,
    ):
        create_category(
            name="Movies",
            description="Movies category",
        )
        non_existing_category_id = uuid.uuid4()
        category_path = f"/api/categories/{non_existing_category_id}/"
        response = client.get(path=category_path)

        assert response.data == {
            "detail": f"Category with {non_existing_category_id} not found."
        }
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCreateCategoryAPI(CommonTestFixtures):
    def test_create_category_when_payload_is_invalid_returns_400(
        self, client: APIClient
    ):
        category_path = "/api/categories/"
        payload = {
            "name": "",
            "description": "Movie description",
        }
        response = client.post(path=category_path, data=payload, format="json")

        assert response.data == {
            "name": [ErrorDetail(string="This field may not be blank.", code="blank")]
        }
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_category_when_payload_is_valid_returns_201(self, client: APIClient):
        category_path = "/api/categories/"
        payload = {
            "name": "Movies",
            "description": "Movie description",
        }
        response = client.post(path=category_path, data=payload, format="json")

        expected_response = {
            "data": {
                "id": response.data["data"]["id"],
                "name": "Movies",
                "description": "Movie description",
                "is_active": True,
            }
        }

        assert response.data == expected_response
        assert response.status_code == status.HTTP_201_CREATED


class TestUpdateCategoryAPI(CommonTestFixtures):
    def test_update_category_when_payload_is_invalid_returns_400(
        self, client: APIClient, create_category
    ):
        category = create_category(
            name="Movies",
            description="Movies category",
        )
        category_path = f"/api/categories/{category.id}/"
        payload = {
            "name": "",
            "description": "Movie description",
        }
        response = client.put(path=category_path, data=payload, format="json")
        assert response.data == {
            "name": [ErrorDetail(string="This field may not be blank.", code="blank")]
        }
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_category_when_payload_is_valid_returns_200(
        self, client: APIClient, create_category
    ):
        category = create_category(
            name="Movies",
            description="Movies category",
        )
        category_path = f"/api/categories/{category.id}/"
        payload = {
            "name": "Movies updated",
            "description": "Movie description updated",
        }
        response = client.put(path=category_path, data=payload, format="json")
        expected_response = {
            "data": {
                "id": str(category.id),
                "name": "Movies updated",
                "description": "Movie description updated",
                "is_active": True,
            }
        }
        assert response.data == expected_response
        assert response.status_code == status.HTTP_200_OK

    def test_return_404_when_category_not_exists(
        self,
        client: APIClient,
    ):
        non_existing_category_id = uuid.uuid4()
        category_path = f"/api/categories/{non_existing_category_id}/"
        payload = {
            "name": "Movies",
            "description": "Movie description",
        }
        response = client.put(path=category_path, data=payload, format="json")
        assert response.data == {
            "detail": f"Can not update category with id: {non_existing_category_id}. Category not found."
        }
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestPartialUpdateCategoryAPI(CommonTestFixtures):
    def test_partial_update_when_payload_is_invalid_returns_400(
        self,
        client: APIClient,
        create_category,
    ):
        category = create_category(
            name="Movies",
            description="Movies category",
        )
        category_path = f"/api/categories/{category.id}/"
        payload = {
            "name": "",
        }
        response = client.patch(path=category_path, data=payload, format="json")
        assert response.data == {
            "name": [ErrorDetail(string="This field may not be blank.", code="blank")]
        }
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_partial_update_when_payload_is_valid_returns_200(
        self,
        client: APIClient,
        create_category,
    ):
        category = create_category(
            name="Movies",
            description="Movies category",
        )
        category_path = f"/api/categories/{category.id}/"
        payload = {
            "name": "Movies updated",
        }
        response = client.patch(path=category_path, data=payload, format="json")
        expected_response = {
            "data": {
                "id": str(category.id),
                "name": "Movies updated",
                "description": "Movies category",
                "is_active": True,
            }
        }
        assert response.data == expected_response
        assert response.status_code == status.HTTP_200_OK


class TestDeleteCategoryAPI(CommonTestFixtures):
    def test_delete_category_when_id_is_not_a_valid_uuid(self, client: APIClient):
        category_path = "/api/categories/invalid-uuid/"
        response = client.delete(path=category_path)
        expected_response = {
            "id": [ErrorDetail(string="Must be a valid UUID.", code="invalid")]
        }
        assert response.data == expected_response
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_category_when_exists(
        self,
        client: APIClient,
        create_category,
        category_repository,
    ):
        category = create_category(
            name="Movies",
            description="Movies category",
        )
        category_path = f"/api/categories/{category.id}/"
        response = client.delete(path=category_path)
        deleted_category = category_repository.get_by_id(category.id)
        assert deleted_category is None
        assert category_repository.list() == []
        assert response.data == {"detail": f"Category deleted successfully."}
        assert response.status_code == status.HTTP_200_OK

    def test_return_404_when_category_not_exists(
        self,
        client: APIClient,
    ):
        non_existing_category_id = uuid.uuid4()
        category_path = f"/api/categories/{non_existing_category_id}/"
        response = client.delete(path=category_path)
        assert response.data == {
            "detail": f"Can not delete Category with id: {non_existing_category_id}. Category not found."
        }
        assert response.status_code == status.HTTP_404_NOT_FOUND
