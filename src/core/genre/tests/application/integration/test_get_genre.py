import uuid
import pytest

from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.genre.application.exceptions import GenreNotFoundException
from src.core.genre.application.use_cases.get_genre import GetGenre
from src.core.genre.domain.genre import Genre


class CommonFixtures:
    @pytest.fixture
    def create_genre(self):
        return lambda name, is_active=True, categories=set(): Genre(
            name=name, is_active=is_active, categories=categories
        )

    @pytest.fixture
    def genre_repository_with_genres(self, create_genre):
        genre_action = create_genre("Action")
        genre_comedy = create_genre("Comedy")
        return (
            InMemoryGenreRepository(genres=[genre_action, genre_comedy]),
            genre_action,
        )

    @pytest.fixture
    def genre_repository_with_no_genres(self):
        return InMemoryGenreRepository(genres=[])


class TestGetGenre(CommonFixtures):
    def test_get_genre_when_genres_exist(self, genre_repository_with_genres):
        genre_repository, genre_action = genre_repository_with_genres
        use_case = GetGenre(repository=genre_repository)
        input = GetGenre.Input(id=genre_action.id)
        output = use_case.execute(input)
        assert output.data.id is not None
        assert output.data.id == genre_action.id
        assert output == GetGenre.Output(data=genre_action)

    def test_get_genre_when_genres_not_exist(self, genre_repository_with_no_genres):
        use_case = GetGenre(repository=genre_repository_with_no_genres)
        invalid_id = uuid.uuid4()
        input = GetGenre.Input(id=invalid_id)
        with pytest.raises(
            GenreNotFoundException, match=f"Genre with id {invalid_id} not found."
        ):
            use_case.execute(input)
