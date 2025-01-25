import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.exceptions import GenreNotFoundException
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class CommonFixtures:
    @pytest.fixture
    def genre_repository(self):
        return InMemoryGenreRepository()

    @pytest.fixture
    def category_repository(self):
        return InMemoryCategoryRepository()

    @pytest.fixture
    def create_category(self):
        return lambda name, is_active=True: Category(name=name, is_active=is_active)

    @pytest.fixture
    def category_movie(self, create_category):
        return create_category("Movie")

    @pytest.fixture
    def category_documentary(self, create_category):
        return create_category("Documentary")

    @pytest.fixture
    def category_tv_show(self, create_category):
        return create_category("TV Show")

    @pytest.fixture
    def create_genre(self):
        return lambda name, is_active=True, categories=set(): Genre(
            name=name, is_active=is_active, categories=categories
        )

    @pytest.fixture
    def genre_action(self, create_genre):
        return create_genre("Action")

    @pytest.fixture
    def category_repository_with_categories(
        self,
        category_movie,
        category_documentary,
        category_tv_show,
        category_repository,
    ):
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        category_repository.save(category_tv_show)
        return category_repository

    @pytest.fixture
    def genre_repository_with_genres(
        self,
        genre_action,
        genre_repository,
    ):
        genre_repository.save(genre_action)
        return genre_repository


class TestUpdateGenre(CommonFixtures):
    def test_update_genre_that_exists(self, genre_repository_with_genres, genre_action):
        use_case = UpdateGenre(repository=genre_repository_with_genres)
        input = UpdateGenre.Input(id=genre_action.id, name="Action Updated")
        output = use_case.execute(input)
        assert output == UpdateGenre.Output(
            id=genre_action.id,
            name=genre_action.name,
            is_active=genre_action.is_active,
            categories=genre_action.categories,
        )

    def test_raises_genre_not_found_exception(self, genre_repository):
        use_case = UpdateGenre(repository=genre_repository)
        non_existing_genre_id = uuid.uuid4()
        input = UpdateGenre.Input(
            id=non_existing_genre_id,
            name="Action Updated",
            categories={uuid.uuid4(), uuid.uuid4()},
        )
        with pytest.raises(
            GenreNotFoundException,
            match=f"Can not update genre with id: {non_existing_genre_id}. Genre not found.",
        ):
            use_case.execute(input)

    def test_update_genre_with_only_name(
        self,
        genre_repository_with_genres,
        genre_action,
    ):
        use_case = UpdateGenre(repository=genre_repository_with_genres)
        input = UpdateGenre.Input(id=genre_action.id, name="Action Updated")
        output = use_case.execute(input)
        assert output.name == "Action Updated"

    def test_update_genre_only_is_active(
        self,
        genre_repository_with_genres,
        genre_action,
    ):
        use_case = UpdateGenre(repository=genre_repository_with_genres)
        input = UpdateGenre.Input(id=genre_action.id, is_active=False)
        output = use_case.execute(input)
        assert not output.is_active

    def test_update_genre_only_categories(
        self,
        category_repository_with_categories,
        genre_repository_with_genres,
        genre_action,
        category_tv_show,
    ):
        use_case = UpdateGenre(
            repository=genre_repository_with_genres,
            category_repository=category_repository_with_categories,
        )
        input = UpdateGenre.Input(
            id=genre_action.id,
            name="Action Updated",
            is_active=genre_action.is_active,
            categories={category_tv_show.id},
        )
        output = use_case.execute(input)
        assert len(output.categories) == 1
        assert genre_action.categories == output.categories
