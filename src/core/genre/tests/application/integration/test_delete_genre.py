import uuid
import pytest

from src.core.genre.application.exceptions import GenreNotFoundException
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.genre.application.use_cases.delete_genre import DeleteGenre


class CommonFixtures:
    @pytest.fixture
    def create_genre(self):
        return lambda name, is_active=True, categories=set(): Genre(
            name=name, is_active=is_active, categories=categories
        )

    @pytest.fixture
    def genre_repository_with_genres(self, create_genre):
        genre_action = create_genre(name="Action")
        genre_adventure = create_genre(name="Adventure")
        genre_comedy = create_genre(name="Comedy")
        genres = [
            genre_action,
            genre_adventure,
            genre_comedy,
        ]
        return (
            InMemoryGenreRepository(genres=genres),
            genre_action,
            genre_adventure,
            genre_comedy,
        )

    @pytest.fixture
    def genre_repository_with_no_genres(self):
        return InMemoryGenreRepository()


class TestDeleteGenre(CommonFixtures):
    def test_delete_genre_from_repository(self, genre_repository_with_genres):
        genre_repository, genre_action, _, _ = genre_repository_with_genres
        use_case = DeleteGenre(repository=genre_repository)
        input = DeleteGenre.Input(id=genre_action.id)
        output = use_case.execute(input)
        assert output == DeleteGenre.Output(detail="Genre deleted successfully.")

    def test_delete_genre_from_repository_with_non_existing_genre(
        self,
        genre_repository_with_no_genres,
    ):
        use_case = DeleteGenre(repository=genre_repository_with_no_genres)
        non_existing_genre_id = uuid.uuid4()
        input = DeleteGenre.Input(id=non_existing_genre_id)
        with pytest.raises(
            GenreNotFoundException,
            match=f"Can not delete Genre with id: {non_existing_genre_id}. Genre not found.",
        ):
            use_case.execute(input)
