from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.abstract_entity import AbstractEntity
from src.core.video.domain.value_objects import AudioVideoMedia, ImageMedia, Rating


@dataclass
class Video(AbstractEntity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    rating: Rating
    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]
    published: bool = False
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None

    def __post_init__(self):
        self._validate()
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def _validate(self):
        if not self.title:
            self.notification.add_error("'title' cannot be empty")
        if len(self.title) > 255:
            self.notification.add_error("'name' cannot be longer than 255 characters.")

    def update(
        self,
        title: str,
        description: str,
        launch_year: int,
        duration: Decimal,
        published: bool,
        rating: Rating,
    ):
        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.published = published
        self.rating = rating
        self._validate()
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)
        return self

    def add_category(self, category_id: UUID) -> None:
        self.categories.add(category_id)
        self._validate()

    def add_genre(self, genre_id: UUID) -> None:
        self.genres.add(genre_id)
        self._validate()

    def add_cast_member(self, cast_member_id: UUID) -> None:
        self.cast_members.add(cast_member_id)
        self._validate()

    def update_banner(self, banner: ImageMedia) -> None:
        self.banner = banner
        self._validate()

    def update_thumbnail(self, thumbnail: ImageMedia) -> None:
        self.thumbnail = thumbnail
        self._validate()

    def update_thumbnail_half(self, thumbnail_half: ImageMedia) -> None:
        self.thumbnail_half = thumbnail_half
        self._validate()

    def update_trailer(self, trailer: AudioVideoMedia) -> None:
        self.trailer = trailer
        self._validate()

    def update_video(self, video: AudioVideoMedia) -> None:
        self.video = video
        self._validate()
