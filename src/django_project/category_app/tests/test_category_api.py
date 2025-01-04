from rest_framework import status
import pytest
from rest_framework.test import APIClient
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


# Create your tests here.
@pytest.mark.django_db
class TestCategoryAPIList:
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

    def test_list_categories(self, client: APIClient, create_category):
        category_movies = create_category(
            name="Movies",
            description="Movies category",
        )
        category_documentary = create_category(
            name="Documentary",
            description="Documentary category",
        )

        url = "/api/categories/"
        response = client.get(url)

        expected_response = [
            {
                "id": str(category_movies.id),
                "name": category_movies.name,
                "description": category_movies.description,
                "is_active": category_movies.is_active,
            },
            {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active,
            },
        ]

        assert response.data == expected_response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        category_movie_response = response.data[0]
        assert category_movie_response["id"] == str(category_movies.id)
        assert category_movie_response["name"] == category_movies.name
        assert category_movie_response["description"] == category_movies.description
        assert category_movie_response["is_active"] == category_movies.is_active

        category_documentary_response = response.data[1]
        assert category_documentary_response["id"] == str(category_documentary.id)
        assert category_documentary_response["name"] == category_documentary.name
        assert (
            category_documentary_response["description"]
            == category_documentary.description
        )
        assert (
            category_documentary_response["is_active"] == category_documentary.is_active
        )

    def test_list_categories_empty(self, client: APIClient):
        url = "/api/categories/"
        response = client.get(url)

        assert response.data == []
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0
