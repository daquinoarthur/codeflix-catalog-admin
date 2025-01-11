# integration test
import uuid
import pytest

from src.core.genre.application.exceptions import GenreNotFoundException
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


# unit test
class CommonFixtures:
    @pytest.fixture
    def create_genre(self):
        return lambda name, is_active=True, categories=set(): Genre(
            name=name, is_active=is_active, categories=categories
        )

    @pytest.fixture
    def genre_repository(self):
        return InMemoryGenreRepository()

    @pytest.fixture
    def genre_repository_with_genres(self, create_genre, genre_repository):
        genre_action = create_genre("Action")
        genre_repository.save(genre_action)
        return genre_repository, genre_action


class TestUpdateGenre(CommonFixtures):
    def test_update_genre_that_exists(self, genre_repository_with_genres):
        genre_repository, genre_action = genre_repository_with_genres
        use_case = UpdateGenre(repository=genre_repository)
        input = UpdateGenre.Input(id=genre_action.id, name="Action Updated")
        output = use_case.execute(input)
        assert output == UpdateGenre.Output(
            id=genre_action.id,
            name=genre_action.name,
            is_active=genre_action.is_active,
            category_ids=genre_action.categories,
        )

    def test_update_genre_that_exists_with_categories(self, genre_repository):
        use_case = UpdateGenre(repository=genre_repository)
        non_existing_genre_id = uuid.uuid4()
        input = UpdateGenre.Input(
            id=non_existing_genre_id,
            name="Action Updated",
            category_ids={uuid.uuid4(), uuid.uuid4()},
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
        assert output.name == "Action Updated"

    def test_update_genre_only_is_active(self, genre_repository_with_genres):
        genre_repository, genre_action = genre_repository_with_genres
        use_case = UpdateGenre(repository=genre_repository)
        input = UpdateGenre.Input(id=genre_action.id, is_active=False)
        output = use_case.execute(input)
        assert not output.is_active

    def test_update_genre_only_categories(self, genre_repository_with_genres):
        genre_repository, genre_action = genre_repository_with_genres
        use_case = UpdateGenre(repository=genre_repository)
        input = UpdateGenre.Input(
            id=genre_action.id, category_ids={uuid.uuid4(), uuid.uuid4()}
        )
        output = use_case.execute(input)
        assert len(output.category_ids) == 2
        assert genre_action.categories == output.category_ids
