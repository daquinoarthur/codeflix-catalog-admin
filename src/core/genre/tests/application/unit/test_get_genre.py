from unittest.mock import create_autospec
import uuid
import pytest

from src.core.genre.application.exceptions import GenreNotFoundException
from src.core.genre.application.use_cases.get_genre import GetGenre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre


class CommonFixtures:
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


class TestGetGenre(CommonFixtures):
    def test_get_genre_when_genres_exist(self, genre_repository_with_genres):
        genre_repository, genre_action = genre_repository_with_genres
        use_case = GetGenre(repository=genre_repository)
        input = GetGenre.Input(id=genre_action.id)
        output = use_case.execute(input)
        assert output == GetGenre.Output(data=genre_action)
        genre_repository.get_by_id.assert_called_once_with(genre_action.id)
        assert genre_repository.get_by_id.call_count == 1

    def test_get_genre_when_genres_not_exist(self, genre_repository_with_no_genres):
        use_case = GetGenre(repository=genre_repository_with_no_genres)
        invalid_id = uuid.uuid4()
        input = GetGenre.Input(id=invalid_id)
        with pytest.raises(
            GenreNotFoundException, match=f"Genre with id {invalid_id} not found."
        ):
            use_case.execute(input)
        genre_repository_with_no_genres.get_by_id.assert_called_once_with(invalid_id)
        assert genre_repository_with_no_genres.get_by_id.call_count == 1
