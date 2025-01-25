import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFoundException
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


# unit test
class CommonFixtures:
    @pytest.fixture
    def create_category(self):
        return lambda name, is_active=True: Category(name=name, is_active=is_active)

    @pytest.fixture
    def category_repository(self):
        return create_autospec(CategoryRepository)

    @pytest.fixture
    def category_repository_with_categories(self, create_category, category_repository):
        category_movie = create_category("Movie")
        category_repository.get_by_id.return_value = category_movie
        return category_repository, category_movie

    @pytest.fixture
    def create_genre(self):
        return lambda name, is_active=True, categories=set(): Genre(
            name=name, is_active=is_active, categories=categories
        )

    @pytest.fixture
    def genre_repository(self):
        return create_autospec(GenreRepository)

    @pytest.fixture
    def genre_repository_with_genres(self, create_genre, genre_repository):
        genre_action = create_genre("Action")
        genre_repository.get_by_id.return_value = genre_action
        return genre_repository, genre_action

    @pytest.fixture
    def genre_repository_with_no_genres(self, genre_repository):
        genre_repository.get_by_id.return_value = None
        return genre_repository


class TestUpdateGenre(CommonFixtures):
    def test_update_genre_that_exists(self, genre_repository_with_genres):
        genre_repository, genre_action = genre_repository_with_genres
        use_case = UpdateGenre(repository=genre_repository)
        input = UpdateGenre.Input(id=genre_action.id, name="Action Updated")
        output = use_case.execute(input)
        genre_repository.get_by_id.assert_called_once_with(genre_action.id)
        genre_repository.update.assert_called_once_with(genre_action)
        assert output == UpdateGenre.Output(
            id=genre_action.id,
            name=genre_action.name,
            is_active=genre_action.is_active,
            categories=genre_action.categories,
        )

    def test_update_genre_that_exists_with_categories(
        self, genre_repository_with_no_genres
    ):
        genre_repository = genre_repository_with_no_genres
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

    def test_update_genre_with_only_name(self, genre_repository_with_genres):
        genre_repository, genre_action = genre_repository_with_genres
        use_case = UpdateGenre(repository=genre_repository)
        input = UpdateGenre.Input(id=genre_action.id, name="Action Updated")
        output = use_case.execute(input)
        genre_repository.get_by_id.assert_called_once_with(genre_action.id)
        genre_repository.update.assert_called_once_with(genre_action)
        assert output.name == "Action Updated"

    def test_update_genre_only_is_active(self, genre_repository_with_genres):
        genre_repository, genre_action = genre_repository_with_genres
        use_case = UpdateGenre(repository=genre_repository)
        input = UpdateGenre.Input(id=genre_action.id, is_active=False)
        output = use_case.execute(input)
        genre_repository.get_by_id.assert_called_once_with(genre_action.id)
        genre_repository.update.assert_called_once_with(genre_action)
        assert not output.is_active

    def test_update_genre_only_categories(
        self, category_repository_with_categories, genre_repository_with_genres
    ):
        genre_repository, genre_action = genre_repository_with_genres
        category_repository, category_movie = category_repository_with_categories
        use_case = UpdateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )
        input = UpdateGenre.Input(
            id=genre_action.id,
            name=genre_action.name,
            is_active=genre_action.is_active,
            categories={category_movie.id},
        )
        output = use_case.execute(input)
        genre_repository.get_by_id.assert_called_once_with(genre_action.id)
        genre_repository.update.assert_called_once_with(genre_action)
        assert output.categories == genre_action.categories
