import uuid
import pytest
from rest_framework import status
from rest_framework.fields import ErrorDetail

from src.core.category.domain.category import Category
from src.core.category.application.use_cases.exceptions import CategoryNotFoundException
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from rest_framework.test import APIClient


@pytest.mark.django_db
class CommonFixtures:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def category_movie(self) -> Category:
        return Category(
            name="Movie",
            description="Movie description",
        )

    @pytest.fixture
    def category_documentary(self) -> Category:
        return Category(
            name="Documentary",
            description="Documentary description",
        )

    @pytest.fixture
    def category_repository(
        self, category_movie, category_documentary
    ) -> DjangoORMCategoryRepository:
        repository = DjangoORMCategoryRepository()
        repository.save(category_movie)
        repository.save(category_documentary)
        return repository

    @pytest.fixture
    def category_repository_empty(self) -> DjangoORMCategoryRepository:
        return DjangoORMCategoryRepository()

    @pytest.fixture
    def genre_romance(self, category_movie, category_documentary):
        return Genre(
            name="Romance",
            is_active=True,
            categories={category_movie.id, category_documentary.id},
        )

    @pytest.fixture
    def genre_drama(self):
        return Genre(
            name="Drama",
            is_active=True,
            categories=set(),
        )

    @pytest.fixture
    def genre_repository(self, genre_romance, genre_drama):
        repository = DjangoORMGenreRepository()
        repository.save(genre_romance)
        repository.save(genre_drama)
        return repository

    @pytest.fixture
    def genre_repository_empty(self) -> DjangoORMGenreRepository:
        return DjangoORMGenreRepository()


class TestListAPI(CommonFixtures):
    def test_list_genres_and_categories(
        self,
        category_repository,
        genre_repository,
        genre_romance,
        genre_drama,
        category_movie,
        category_documentary,
        client,
    ):
        list_genres_path = "/api/genres/"
        response = client.get(path=list_genres_path)
        genre_romance_response = response.data["data"][0]
        assert genre_romance_response["id"] == str(genre_romance.id)
        assert genre_romance_response["name"] == genre_romance.name
        assert genre_romance_response["is_active"] == genre_romance.is_active
        assert set(genre_romance_response["categories"]) == {
            str(category_movie.id),
            str(category_documentary.id),
        }
        genre_drama_response = response.data["data"][1]
        assert genre_drama_response["id"] == str(genre_drama.id)
        assert genre_drama_response["name"] == genre_drama.name
        assert genre_drama_response["is_active"] == genre_drama.is_active
        assert genre_drama_response["categories"] == []


class TestRetrieveAPI(CommonFixtures):
    def test_retrieve_genre_successfully(
        self,
        client,
        category_repository,
        genre_repository,
        category_movie,
        category_documentary,
        genre_romance,
    ):
        retrieve_genre_path = f"/api/genres/{genre_romance.id}/"
        response = client.get(path=retrieve_genre_path)
        assert response.data["id"] == str(genre_romance.id)
        assert response.data["name"] == genre_romance.name
        assert response.data["is_active"] == genre_romance.is_active
        assert set(response.data["categories"]) == {
            str(category_movie.id),
            str(category_documentary.id),
        }
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_genre_with_invalid_pk(self, client):
        invalid_genre_id = "invalid_uuid"
        retrieve_genre_path = f"/api/genres/{invalid_genre_id}/"
        response = client.get(path=retrieve_genre_path)
        assert response.data == {
            "id": [ErrorDetail(string="Must be a valid UUID.", code="invalid")]
        }
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_genre_when_genre_does_not_exist(self, client):
        non_existing_genre_id = uuid.uuid4()
        retrieve_genre_path = f"/api/genres/{non_existing_genre_id}/"
        response = client.get(path=retrieve_genre_path)
        assert response.data == {
            "detail": f"Genre with id {non_existing_genre_id} not found."
        }
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCreateGenreAPI(CommonFixtures):
    def test_create_genre_with_associated_categories(
        self,
        category_repository,
        genre_repository_empty,
        client,
        category_movie,
        category_documentary,
    ):
        create_genre_path = "/api/genres/"
        payload = {
            "name": "Action",
            "is_active": True,
            "categories": [str(category_movie.id), str(category_documentary.id)],
        }
        response = client.post(path=create_genre_path, data=payload, format="json")
        created_genre = genre_repository_empty.get_by_id(response.data["id"])
        assert len(genre_repository_empty.list()) == 1
        assert created_genre.name == payload["name"]
        assert created_genre.is_active == payload["is_active"]
        assert created_genre.categories == {category_movie.id, category_documentary.id}

    def test_create_genre_when_categories_do_not_exist(self, client):
        create_genre_path = "/api/genres/"
        non_existing_category_id = uuid.uuid4()
        payload = {
            "name": "Action",
            "is_active": True,
            "categories": [non_existing_category_id],
        }
        response = client.post(path=create_genre_path, data=payload, format="json")
        assert response.status_code == 400
        assert response.data == {
            "error": f"Related categories not found: {set(payload['categories'])}. Cannot create genre."
        }


class TestPartialUpdateAPI(CommonFixtures):
    def test_partial_update_genre(
        self,
        client,
        category_repository,
        genre_repository,
        category_movie,
        category_documentary,
        genre_romance,
    ):
        partial_update_path = f"/api/genres/{genre_romance.id}/"
        payload = {
            "name": "Romantic Updated",
        }
        response = client.patch(
            path=partial_update_path,
            data=payload,
            format="json",
        )
        assert response.data["id"] == str(genre_romance.id)
        assert response.data["name"] == "Romantic Updated"
        assert response.data["is_active"] == True
        assert set(response.data["categories"]) == {
            str(category_movie.id),
            str(category_documentary.id),
        }

    def test_partial_update_genre_with_non_existing_genre(self, client):
        non_existing_genre_id = uuid.uuid4()
        partial_update_path = f"/api/genres/{non_existing_genre_id}/"
        payload = {
            "name": "Romantic Updated",
        }
        response = client.patch(
            path=partial_update_path,
            data=payload,
            format="json",
        )
        assert response.data == {
            "detail": f"Can not update genre with id: {non_existing_genre_id}. Genre not found."
        }
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_partial_update_genre_with_invalid_pk(self, client):
        invalid_genre_id = "invalid_uuid"
        partial_update_path = f"/api/genres/{invalid_genre_id}/"
        payload = {
            "name": "Romantic Updated",
        }
        response = client.patch(
            path=partial_update_path,
            data=payload,
            format="json",
        )
        assert response.data == {
            "id": [ErrorDetail(string="Must be a valid UUID.", code="invalid")]
        }
        assert response.status_code == 400

    def test_partial_update_genre_with_invalid_data(
        self,
        category_repository,
        genre_repository,
        client,
        genre_romance,
    ):
        partial_update_path = f"/api/genres/{genre_romance.id}/"
        payload = {
            "categories": 1,
        }
        response = client.patch(
            path=partial_update_path,
            data=payload,
            format="json",
        )
        assert response.data == {
            "categories": [
                ErrorDetail(
                    string='Expected a list of items but got type "int".',
                    code="not_a_list",
                )
            ]
        }
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_partial_update_with_non_existing_category(
        self,
        client,
        category_repository,
        genre_repository,
        genre_romance,
    ):
        partial_update_path = f"/api/genres/{genre_romance.id}/"
        non_existing_category_id = uuid.uuid4()
        payload = {
            "categories": [str(non_existing_category_id)],
        }
        response = client.patch(
            path=partial_update_path,
            data=payload,
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteGenreAPI(CommonFixtures):
    def test_when_genre_does_not_exist_then_raise_404(self, client):
        non_existing_genre_id = uuid.uuid4()
        delete_genre_path = f"/api/genres/{non_existing_genre_id}/"
        response = client.delete(path=delete_genre_path)
        assert response.status_code == 404
        assert response.data == {
            "detail": f"Can not delete Genre with id: {non_existing_genre_id}. Genre not found."
        }

    def test_delete_genre_when_it_exists(
        self,
        client,
        category_repository,
        genre_repository,
        genre_romance,
        genre_drama,
    ):
        delete_genre_path = f"/api/genres/{genre_romance.id}/"
        response = client.delete(path=delete_genre_path)
        assert response.data == {"detail": "Genre deleted successfully."}
        assert response.status_code == status.HTTP_200_OK

    def test_delete_genre_with_invalid_pk(self, client):
        delete_genre_path = f"/api/genres/invalid_uuid/"
        response = client.delete(path=delete_genre_path)
        assert response.status_code == 400
        assert response.data == {
            "id": [ErrorDetail(string="Must be a valid UUID.", code="invalid")]
        }


class TestUpdateGenreAPI(CommonFixtures):
    def test_when_request_data_with_categories_is_valid_then_update_genre(
        self,
        category_repository,
        genre_repository,
        category_movie,
        category_documentary,
        client,
        genre_romance,
    ):
        update_genre_path = f"/api/genres/{genre_romance.id}/"
        payload = {
            "name": "Romantic Updated",
            "is_active": False,
            "categories": [category_movie.id, category_documentary.id],
        }
        response = client.put(path=update_genre_path, data=payload, format="json")
        assert response.data["id"] == str(genre_romance.id)
        assert response.data["name"] == payload["name"]
        assert response.data["is_active"] == payload["is_active"]
        assert set(response.data["categories"]) == {
            str(category_movie.id),
            str(category_documentary.id),
        }

    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository,
        genre_repository,
        client,
        genre_romance,
    ):
        update_genre_path = f"/api/genres/{genre_romance.id}/"
        payload = {
            "name": "Romantic Updated",
            "is_active": False,
            "categories": [],
        }
        response = client.put(path=update_genre_path, data=payload, format="json")
        assert response.data == {
            "id": str(genre_romance.id),
            "name": "Romantic Updated",
            "is_active": False,
            "categories": [],
        }

    def test_when_request_data_is_invalid_then_return_400(
        self,
        category_repository,
        genre_repository,
        client,
        genre_romance,
    ):
        update_genre_path = f"/api/genres/{genre_romance.id}/"
        payload = {
            "name": "Romantic Updated",
            "is_active": False,
            "categories": 1,
        }
        response = client.put(path=update_genre_path, data=payload, format="json")
        assert response.data == {
            "categories": [
                ErrorDetail(
                    string='Expected a list of items but got type "int".',
                    code="not_a_list",
                )
            ]
        }
        assert response.status_code == 400

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository,
        genre_repository,
        client,
        genre_romance,
    ):
        update_genre_path = f"/api/genres/{genre_romance.id}/"
        non_existing_category_id = uuid.uuid4()
        payload = {
            "name": "Romantic Updated",
            "is_active": False,
            "categories": [str(non_existing_category_id)],
        }
        with pytest.raises(
            CategoryNotFoundException,
            match=f"Cannot update genre, related categories not found.",
        ):
            client.put(path=update_genre_path, data=payload, format="json")

    def test_when_genre_does_not_exist_then_return_404(self, client):
        non_existing_genre_id = uuid.uuid4()
        update_genre_path = f"/api/genres/{non_existing_genre_id}/"
        payload = {
            "name": "Romantic Updated",
            "is_active": False,
            "categories": [],
        }
        response = client.put(path=update_genre_path, data=payload, format="json")
        assert response.data == {
            "detail": f"Can not update genre with id: {non_existing_genre_id}. Genre not found."
        }
        assert response.status_code == 404
