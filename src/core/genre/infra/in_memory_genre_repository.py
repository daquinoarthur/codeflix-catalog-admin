from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class InMemoryGenreRepository(GenreRepository):
    def __init__(self, genres: list[Genre] | None = None):
        self.genres = genres or []

    def save(self, genre) -> Genre:
        self.genres.append(genre)
        return genre

    def get_by_id(self, id) -> Genre | None:
        return next((genre for genre in self.genres if genre.id == id), None)

    def delete(self, id) -> None:
        self.genres = [genre for genre in self.genres if genre.id != id]

    def update(self, genre) -> Genre:
        self.genres.remove(genre)
        self.genres.append(genre)
        return genre

    def list(self) -> list[Genre]:
        return [genre for genre in self.genres]
