from unittest.mock import create_autospec
import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import (
    InvalidGenreDataException,
    RelatedCategoriesNotFoundException,
)
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class CommonFixtures:
    @pytest.fixture
    def mock_genre_repository(self):
        return create_autospec(GenreRepository)

    @pytest.fixture
    def movie_category(self):
        return Category(name="Movie")

    @pytest.fixture
    def documentary_category(self):
        return Category(name="Documentary")

    @pytest.fixture
    def mock_category_repository_with_categories(
        self, movie_category, documentary_category
    ):
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = [
            movie_category,
            documentary_category,
        ]
        return repository

    @pytest.fixture
    def mock_empty_category_repository(self):
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = []
        return repository


class TestCreateGenre(CommonFixtures):
    def test_when_categories_do_not_exist_then_raise_related_categories_not_found(
        self,
        mock_empty_category_repository,
        mock_genre_repository,
    ):
        use_case = CreateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_empty_category_repository,
        )
        category_id = uuid.uuid4()
        input = CreateGenre.Input(
            name="Action",
            category_ids={category_id},
        )
        with pytest.raises(RelatedCategoriesNotFoundException) as exc_info:
            use_case.execute(input)
        assert str(category_id) in str(exc_info.value)

    def test_when_created_genre_is_invalid_then_raise_invalid_genre(
        self,
        movie_category,
        mock_category_repository_with_categories,
        mock_genre_repository,
    ):
        use_case = CreateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )
        input = CreateGenre.Input(
            name="",
            category_ids={movie_category.id},
        )
        with pytest.raises(InvalidGenreDataException) as exc_info:
            use_case.execute(input)
        assert exc_info.value.args[0] == "Name cannot be empty."

    def test_when_created_genre_is_valid_and_categories_exist_then_save_genre(
        self,
        movie_category,
        documentary_category,
        mock_category_repository_with_categories,
        mock_genre_repository,
    ):
        use_case = CreateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids={movie_category.id, documentary_category.id},
        )
        output = use_case.execute(input)
        assert output.id is not None
        assert isinstance(output.id, uuid.UUID)
        saved_genre = mock_genre_repository.save.call_args[0][0]
        assert saved_genre.id == output.id
        assert saved_genre.name == "Action"  # Not "Action Arthur"
        assert saved_genre.categories == {movie_category.id, documentary_category.id}
        assert saved_genre.is_active == True

    def test_create_genre_without_categories(
        self,
        mock_empty_category_repository,
        mock_genre_repository,
    ):
        use_case = CreateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_empty_category_repository,
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids=set(),
        )
        output = use_case.execute(input)
        assert output.id is not None
        assert isinstance(output.id, uuid.UUID)
        saved_genre = mock_genre_repository.save.call_args[0][0]
        assert saved_genre.id == output.id
        assert saved_genre.name == "Action"
        assert saved_genre.categories == set()
        assert saved_genre.is_active == True
