import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.exceptions import (
    InvalidGenreDataException,
    RelatedCategoriesNotFoundException,
)
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class CommonFixtures:
    @pytest.fixture
    def movie_category(self):
        return Category(name="Movie")

    @pytest.fixture
    def documentary_category(self):
        return Category(name="Documentary")


class TestCreateGenre(CommonFixtures):
    def test_when_categories_do_not_exist_then_raise_related_categories_not_found(
        self,
    ):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()
        use_case = CreateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )
        category_id = uuid.uuid4()
        input = CreateGenre.Input(
            name="Action",
            category_ids={category_id},
        )
        with pytest.raises(RelatedCategoriesNotFoundException) as exc_info:
            use_case.execute(input)
        assert str(category_id) in str(exc_info.value)
        assert (
            str(exc_info.value)
            == f"Related categories not found: {{UUID('{category_id}')}}. Cannot create genre."
        )

    def test_when_created_genre_is_invalid_then_raise_invalid_genre(
        self,
        movie_category,
        documentary_category,
    ):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository(
            categories=[movie_category, documentary_category],
        )
        use_case = CreateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
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
    ):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository(
            categories=[movie_category, documentary_category],
        )
        use_case = CreateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids={movie_category.id, documentary_category.id},
        )
        output = use_case.execute(input)
        assert output.id is not None
        assert isinstance(output.id, uuid.UUID)
        assert output.name == "Action"
        assert output.categories == {movie_category.id, documentary_category.id}
        assert output.is_active == True

    def test_create_genre_without_categories(
        self,
    ):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()
        use_case = CreateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids=set(),
        )
        output = use_case.execute(input)
        assert output.id is not None
        assert isinstance(output.id, uuid.UUID)
        assert output.id == output.id
        assert output.name == "Action"
        assert output.categories == set()
        assert output.is_active == True
        assert genre_repository.get_by_id(output.id) is not None
