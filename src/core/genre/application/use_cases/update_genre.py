from dataclasses import dataclass
from uuid import UUID
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.exceptions import (
    GenreNotFoundException,
    InvalidGenreDataException,
)


class UpdateGenre:
    @dataclass
    class Input:
        id: UUID
        name: str | None = None
        is_active: bool = True
        category_ids: set[UUID] | None = None

    @dataclass
    class Output:
        id: UUID
        name: str
        is_active: bool
        category_ids: set[UUID]

    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        genre = self.repository.get_by_id(input.id)
        if not genre:
            raise GenreNotFoundException(
                f"Can not update genre with id: {input.id}. Genre not found."
            )
        try:
            genre.change_name(input.name) if input.name else None
            for category_id in input.category_ids or []:
                genre.add_category(category_id)
            genre.activate() if input.is_active else genre.deactivate()
        except InvalidGenreDataException as error:
            raise InvalidGenreDataException(str(error))
        self.repository.update(genre)
        return UpdateGenre.Output(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            category_ids=genre.categories,
        )
