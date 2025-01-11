from dataclasses import dataclass
from uuid import UUID

from src.core.genre.application.exceptions import GenreNotFoundException
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class GetGenre:
    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        data: Genre

    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        genre = self.repository.get_by_id(input.id)
        if genre is None:
            raise GenreNotFoundException(f"Genre with id {input.id} not found.")
        return self.Output(data=genre)
