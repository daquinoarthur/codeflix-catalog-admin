from dataclasses import dataclass
from uuid import UUID
from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreData:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]


class ListGenre:
    @dataclass
    class Input: ...

    @dataclass
    class Output:
        data: list[GenreData]

    def __init__(self, repository: GenreRepository):
        self.genre_repository = repository

    def execute(self, input: Input) -> Output:
        genres = self.genre_repository.list()
        return self.Output(
            data=[
                GenreData(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                )
                for genre in genres
            ],
        )
