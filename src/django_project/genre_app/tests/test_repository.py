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
