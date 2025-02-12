from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.notification import Notification
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.use_cases.exceptions import (
    InvalidVideoDataException,
    RelatedEntitiesNotFoundException,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


@dataclass
class CreateVideoWithoutMedia:
    @dataclass
    class Input:
        title: str
        description: str
        launch_year: int
        duration: Decimal
        rating: Rating
        categories: set[UUID]
        genres: set[UUID]
        cast_members: set[UUID]

    @dataclass
    class Output:
        id: UUID
        title: str
        description: str
        launch_year: int
        duration: Decimal
        published: bool
        rating: Rating
        categories: set[UUID]
        genres: set[UUID]
        cast_members: set[UUID]

    def __init__(
        self,
        repository: VideoRepository,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ) -> None:
        self.repository = repository
        self.category_repository = category_repository
        self.genre_repository = genre_repository
        self.cast_member_repository = cast_member_repository

    def execute(self, input: Input) -> Output:
        notification = Notification()
        self._validate_categories(input, notification)
        self._validate_genres(input, notification)
        self._validate_cast_members(input, notification)
        if notification.has_errors:
            raise RelatedEntitiesNotFoundException(notification.messages)
        try:
            video = Video(
                title=input.title,
                description=input.description,
                launch_year=input.launch_year,
                duration=input.duration,
                rating=input.rating,
                categories=input.categories,
                genres=input.genres,
                cast_members=input.cast_members,
            )
        except ValueError as e:
            raise InvalidVideoDataException(str(e))
        persisted_video = self.repository.save(video)
        return self.Output(
            id=persisted_video.id,
            title=persisted_video.title,
            description=persisted_video.description,
            launch_year=persisted_video.launch_year,
            duration=persisted_video.duration,
            published=persisted_video.published,
            rating=persisted_video.rating,
            categories={category.id for category in persisted_video.categories.all()},
            genres={genre.id for genre in persisted_video.genres.all()},
            cast_members={
                cast_member.id for cast_member in persisted_video.cast_members.all()
            },
        )

    def _validate_categories(self, input: Input, notification: Notification):
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(category_ids):
            notification.add_error(
                f"Categories with the provided IDs not found {input.categories - category_ids}"
            )

    def _validate_genres(self, input: Input, notification: Notification):
        genre_ids = {genre.id for genre in self.genre_repository.list()}
        if not input.genres.issubset(genre_ids):
            notification.add_error(
                f"Genres with the provided IDs not found {input.genres - genre_ids}"
            )

    def _validate_cast_members(self, input: Input, notification: Notification):
        cast_member_ids = {
            cast_member.id for cast_member in self.cast_member_repository.list()
        }
        if not input.cast_members.issubset(cast_member_ids):
            notification.add_error(
                f"Cast Members with the provided IDs not found {input.cast_members - cast_member_ids}"
            )
