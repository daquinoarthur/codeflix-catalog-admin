from unittest.mock import create_autospec
import pytest

from src.core.genre.application.use_cases.list_genre import GenreData, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class CommonFixtures:
    @pytest.fixture
    def create_genre(self):
        return lambda name, is_active=True, categories=set(): Genre(
            name=name, is_active=is_active, categories=categories
        )

    @pytest.fixture
    def mock_genre_repository_with_genres(self, create_genre):
        repository = create_autospec(GenreRepository)
        genre_action = create_genre("Action")
        genre_adventure = create_genre("Adventure")
        repository.list.return_value = [genre_action, genre_adventure]
        return repository, genre_action, genre_adventure

    @pytest.fixture
    def mock_genre_repository_without_genres(self):
        repository = create_autospec(GenreRepository)
        repository.list.return_value = []
        return repository


class TestDeleteGenre(CommonFixtures):
    def test_list_genres_with_associated_categories(
        self,
        mock_genre_repository_with_genres,
    ):
        repository, genre_action, genre_adventure = mock_genre_repository_with_genres
        use_case = ListGenre(repository=repository)
        input = ListGenre.Input()
        output = use_case.execute(input)
        assert output == ListGenre.Output(
            data=[
                GenreData(
                    id=genre_action.id,
                    name="Action",
                    is_active=True,
                    categories=set(),
                ),
                GenreData(
                    id=genre_adventure.id,
                    name="Adventure",
                    is_active=True,
                    categories=set(),
                ),
            ]
        )
        assert len(output.data) == 2
        repository.list.assert_called_once()

    def test_list_genres_without_associated_categories(
        self, mock_genre_repository_without_genres
    ):
        use_case = ListGenre(repository=mock_genre_repository_without_genres)
        input = ListGenre.Input()
        output = use_case.execute(input)
        assert output == ListGenre.Output(data=[])
        assert len(output.data) == 0
        mock_genre_repository_without_genres.list.assert_called_once()
