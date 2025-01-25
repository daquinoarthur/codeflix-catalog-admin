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

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre = self.genre_model.objects.get(id=id)
        except self.genre_model.DoesNotExist:
            return None
        return Genre(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories={category.id for category in genre.categories.all()},
        )

    def delete(self, id: UUID) -> None:
        self.genre_model.objects.filter(id=id).delete()

    def list(self) -> list[Genre]:
        return [
            Genre(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories={category.id for category in genre.categories.all()},
            )
            for genre in self.genre_model.objects.all()
        ]

    def update(self, genre: Genre) -> Genre | None:
        try:
            with transaction.atomic():
                persisted_genre = self.genre_model.objects.select_for_update().get(
                    id=genre.id
                )
                update_fields = {
                    "name": genre.name,
                    "is_active": genre.is_active,
                }
                self.genre_model.objects.filter(id=genre.id).update(**update_fields)
                persisted_genre.categories.set(genre.categories)
                persisted_genre.refresh_from_db()
                return Genre(
                    id=persisted_genre.id,
                    name=persisted_genre.name,
                    is_active=persisted_genre.is_active,
                    categories={
                        category.id for category in persisted_genre.categories.all()
                    },
                )
        except self.genre_model.DoesNotExist:
            return None
