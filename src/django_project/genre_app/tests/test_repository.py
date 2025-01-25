import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import Genre as GenreModel


@pytest.mark.django_db
class TestSave:
    def test_saves_genre_in_database(self):
        genre = Genre(
            name="Action",
            is_active=True,
            categories=set(),
        )
        repository = DjangoORMGenreRepository()
        assert GenreModel.objects.all().count() == 0
        created_genre = repository.save(genre)
        assert GenreModel.objects.all().count() == 1
        assert created_genre == genre
        assert created_genre.id == genre.id
        assert created_genre.name == genre.name
        assert created_genre.is_active == genre.is_active

    def test_saves_genre_with_categories_in_database(self):
        genre_repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()
        category_action = category_repository.save(Category(name="Action"))
        category_adventure = category_repository.save(Category(name="Adventure"))
        genre = Genre(
            name="Action",
            is_active=True,
            categories={category_action.id, category_adventure.id},
        )
        assert GenreModel.objects.all().count() == 0
        created_genre = genre_repository.save(genre)
        assert GenreModel.objects.all().count() == 1
        assert created_genre == genre
        assert created_genre.id == genre.id
        assert created_genre.name == genre.name
        assert created_genre.is_active == genre.is_active
        categories = created_genre.categories.all().values_list("id", flat=True)
        assert category_action.id in categories
        assert category_adventure.id in categories


@pytest.mark.django_db
class TestGetById:
    def test_returns_genre_by_id(self):
        genre_repository = DjangoORMGenreRepository()
        genre = genre_repository.save(
            Genre(name="Action", is_active=True, categories=set())
        )
        assert genre_repository.get_by_id(genre.id) == genre

    def test_returns_none_when_genre_does_not_exist(self):
        genre_repository = DjangoORMGenreRepository()
        non_existing_genre_id = uuid.uuid4()
        assert genre_repository.get_by_id(non_existing_genre_id) is None


@pytest.mark.django_db
class TestListGenres:
    def test_returns_list_of_genres(self):
        genre_repository = DjangoORMGenreRepository()
        genre1 = genre_repository.save(
            Genre(name="Action", is_active=True, categories=set())
        )
        genre2 = genre_repository.save(
            Genre(name="Adventure", is_active=True, categories=set())
        )
        assert genre_repository.list() == [genre1, genre2]

    def test_returns_empty_list_when_no_genres(self):
        genre_repository = DjangoORMGenreRepository()
        assert genre_repository.list() == []


@pytest.mark.django_db
class TestUpdate:
    def test_updates_genre(self):
        genre_repository = DjangoORMGenreRepository()
        genre = genre_repository.save(
            Genre(name="Action", is_active=True, categories=set())
        )
        genre.name = "Adventure"
        genre.is_active = False
        updated_genre = genre_repository.update(genre)
        assert updated_genre == genre
        assert updated_genre.id == genre.id
        assert updated_genre.name == genre.name
        assert updated_genre.is_active == genre.is_active

    def test_returns_none_when_genre_does_not_exist(self):
        genre_repository = DjangoORMGenreRepository()
        non_existing_genre = Genre(
            id=uuid.uuid4(), name="Action", is_active=True, categories=set()
        )
        assert genre_repository.update(non_existing_genre) is None


@pytest.mark.django_db
class TestDelete:
    def test_deletes_genre(self):
        genre_repository = DjangoORMGenreRepository()
        genre = genre_repository.save(
            Genre(name="Action", is_active=True, categories=set())
        )
        assert GenreModel.objects.all().count() == 1
        genre_repository.delete(genre.id)
        assert GenreModel.objects.all().count() == 0

    def test_does_not_fail_when_genre_does_not_exist(self):
        genre_repository = DjangoORMGenreRepository()
        non_existing_genre_id = uuid.uuid4()
        assert GenreModel.objects.all().count() == 0
        genre_repository.delete(non_existing_genre_id)
        assert GenreModel.objects.all().count() == 0
