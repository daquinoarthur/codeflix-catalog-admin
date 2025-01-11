from uuid import UUID

from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreModel


class DjangoORMGenreRepository(GenreRepository):
    def __init__(self, genre_model: GenreModel | None = None):
        self.genre_model = genre_model or GenreModel

    def save(self, genre: Genre) -> Genre:
        with transaction.atomic():
            persisted_genre = self.genre_model.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
            )
            persisted_genre.categories.set(genre.categories)
        return Genre(
            id=persisted_genre.id,
            name=persisted_genre.name,
            is_active=persisted_genre.is_active,
            categories=persisted_genre.categories.all(),
        )

    def get_by_id(self, id: UUID) -> Genre | None: ...

    def delete(self, id: UUID) -> None: ...

    def update(self, genre: Genre) -> Genre: ...

    def list(self) -> list[Genre]: ...
