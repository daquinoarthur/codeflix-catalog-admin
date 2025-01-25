from dataclasses import dataclass
from uuid import UUID

from src.core.genre.application.exceptions import GenreNotFoundException
from src.core.genre.domain.genre_repository import GenreRepository


class DeleteGenre:
    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        detail: str

    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        genre = self.repository.get_by_id(input.id)
        if genre is None:
            raise GenreNotFoundException(
                f"Can not delete Genre with id: {input.id}. Genre not found."
            )
        self.repository.delete(genre.id)
        return self.Output(detail="Genre deleted successfully.")
