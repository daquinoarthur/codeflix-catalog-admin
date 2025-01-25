import uuid
import pytest
from unittest.mock import create_autospec

from src.core.genre.application.exceptions import GenreNotFoundException
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class TestDeleteGenre:
    @pytest.fixture
    def mock_genre_repository(self):
        return create_autospec(GenreRepository)

    def test_delete_genre_from_repository(self, mock_genre_repository):
        genre = Genre(name="Action")
        mock_genre_repository.get_by_id.return_value = genre
        use_case = DeleteGenre(repository=mock_genre_repository)
        input = DeleteGenre.Input(id=genre.id)
        output = use_case.execute(input)
        assert output == DeleteGenre.Output(detail="Genre deleted successfully.")
        mock_genre_repository.get_by_id.assert_called_once_with(genre.id)
        mock_genre_repository.delete.assert_called_once_with(genre.id)

    def test_delete_genre_from_repository_with_non_existing_genre(
        self,
        mock_genre_repository,
    ):
        mock_genre_repository.get_by_id.return_value = None
        use_case = DeleteGenre(repository=mock_genre_repository)
        wrong_genre_id = uuid.uuid4()
        input = DeleteGenre.Input(id=wrong_genre_id)
        with pytest.raises(
            GenreNotFoundException,
            match=f"Can not delete Genre with id: {wrong_genre_id}. .*.",
        ):
            use_case.execute(input)
