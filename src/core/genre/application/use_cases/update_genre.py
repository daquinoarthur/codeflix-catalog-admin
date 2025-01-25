from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.use_cases.exceptions import CategoryNotFoundException
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.exceptions import (
    GenreNotFoundException,
    InvalidGenreDataException,
)


class UpdateGenre:
    @dataclass
    class Input:
        id: UUID
        name: str = ""
        is_active: bool = True
        categories: set[UUID] | None = None

    @dataclass
    class Output:
        id: UUID
        name: str
        is_active: bool
        categories: set[UUID]

    def __init__(
        self,
        repository: GenreRepository,
        category_repository: CategoryRepository | None = None,
    ):
        self.repository = repository
        self.category_repository = category_repository

    def execute(self, input: Input) -> Output:
        genre = self.repository.get_by_id(input.id)
        if not genre:
            raise GenreNotFoundException(
                f"Can not update genre with id: {input.id}. Genre not found."
            )
        if input.categories and not self._categories_exist(
            self.category_repository,
            input.categories,
        ):
            raise CategoryNotFoundException(
                f"Cannot update genre, related categories not found."
            )
        try:
            genre.change_name(input.name) if input.name else None
            if type(input.categories) == set:
                genre.categories.clear()
                if input.categories:
                    for category_id in input.categories:
                        genre.add_category(category_id)
            genre.activate() if input.is_active else genre.deactivate()
        except InvalidGenreDataException as error:
            raise InvalidGenreDataException(str(error))
        self.repository.update(genre)
        return UpdateGenre.Output(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories=genre.categories,
        )

    def _categories_exist(self, category_repository, categories: set[UUID]) -> bool:
        return all(
            category_repository.get_by_id(category_id) for category_id in categories
        )
