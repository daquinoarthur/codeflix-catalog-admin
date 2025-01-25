from dataclasses import dataclass, field
from uuid import UUID

from src.core.genre.application.exceptions import (
    InvalidGenreDataException,
    RelatedCategoriesNotFoundException,
)
from src.core.genre.domain.genre import Genre


class CreateGenre:
    @dataclass
    class Input:
        name: str
        category_ids: set[UUID] = field(default_factory=set)
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID
        name: str
        categories: set[UUID]
        is_active: bool

    def __init__(self, genre_repository, category_repository):
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    def execute(self, input: Input) -> Output:
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.category_ids.issubset(category_ids):
            raise RelatedCategoriesNotFoundException(
                f"Related categories not found: {input.category_ids - category_ids}. Cannot create genre."
            )
        try:
            genre = Genre(
                name=input.name,
                is_active=input.is_active,
                categories={category_id for category_id in input.category_ids},
            )
        except ValueError as e:
            raise InvalidGenreDataException(str(e)) from e
        self.genre_repository.save(genre)
        return self.Output(
            id=genre.id,
            name=genre.name,
            categories=genre.categories,
            is_active=genre.is_active,
        )
