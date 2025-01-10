import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.use_cases.list_genre import GenreData, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.mark.django_db
class CommonFixtures:
    @pytest.fixture
    def movie_category(self):
        return Category(name="Movie")

    @pytest.fixture
    def documentary_category(self):
        return Category(name="Documentary")

    @pytest.fixture
    def action_genre_with_categories(self, movie_category, documentary_category):
        return Genre(
            name="Action", categories={movie_category.id, documentary_category.id}
        )

    @pytest.fixture
    def action_genre_without_categories(self):
        return Genre(name="Action")

    @pytest.fixture
    def drama_genre_with_categories(self, movie_category):
        return Genre(name="Drama", categories={movie_category.id})

    @pytest.fixture
    def drama_genre_without_categories(self):
        return Genre(name="Drama")


class TestListGenres(CommonFixtures):
    def test_list_genres_with_associated_categories(
        self,
        movie_category,
        documentary_category,
        action_genre_with_categories,
        drama_genre_with_categories,
    ):
        InMemoryCategoryRepository([movie_category, documentary_category])
        genre_repository = InMemoryGenreRepository(
            [action_genre_with_categories, drama_genre_with_categories]
        )
        use_case = ListGenre(genre_repository)
        input = ListGenre.Input()
        output = use_case.execute(input)
        assert len(output.data) == 2
        assert output == ListGenre.Output(
            data=[
                GenreData(
                    id=action_genre_with_categories.id,
                    name="Action",
                    is_active=True,
                    categories={movie_category.id, documentary_category.id},
                ),
                GenreData(
                    id=drama_genre_with_categories.id,
                    name="Drama",
                    is_active=True,
                    categories={movie_category.id},
                ),
            ]
        )

    def test_list_genres_without_associated_categories(
        self, action_genre_without_categories, drama_genre_without_categories
    ):
        genre_repository = InMemoryGenreRepository(
            [action_genre_without_categories, drama_genre_without_categories]
        )
        use_case = ListGenre(genre_repository)
        input = ListGenre.Input()
        output = use_case.execute(input)
        assert len(output.data) == 2
        assert output == ListGenre.Output(
            data=[
                GenreData(
                    id=action_genre_without_categories.id,
                    name="Action",
                    is_active=True,
                    categories=set(),
                ),
                GenreData(
                    id=drama_genre_without_categories.id,
                    name="Drama",
                    is_active=True,
                    categories=set(),
                ),
            ]
        )

    def test_list_genres_with_no_genres(self):
        genre_repository = InMemoryGenreRepository([])
        use_case = ListGenre(genre_repository)
        input = ListGenre.Input()
        output = use_case.execute(input)
        assert len(output.data) == 0
        assert output == ListGenre.Output(data=[])
