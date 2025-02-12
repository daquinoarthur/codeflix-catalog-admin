from uuid import UUID
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.django_project.video_app.models import Video as VideoModel


class DjangoORMVideoRepository(VideoRepository):
    def __init__(self, model: VideoModel | None = None) -> None:
        self.model = model or VideoModel

    def save(self, video: Video) -> Video:
        persisted_video = VideoModelMapper.from_entity_to_model(video)
        return VideoModelMapper.from_model_to_entity(persisted_video)

    def get_by_id(self, id: UUID) -> Video | None:
        raise NotImplementedError

    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    def list(self) -> list[Video]:
        raise NotImplementedError

    def update(self, video: Video) -> Video | None:
        raise NotImplementedError


class VideoModelMapper:
    @staticmethod
    def from_entity_to_model(video: Video) -> VideoModel:
        model = VideoModel(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            published=video.published,
            rating=video.rating,
        )
        model.save()
        if video.categories:
            model.categories.set(video.categories)
        if video.genres:
            model.genres.set(video.genres)
        if video.cast_members:
            model.cast_members.set(video.cast_members)
        return model

    @staticmethod
    def from_model_to_entity(video: VideoModel) -> Video:
        return Video(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            published=video.published,
            rating=video.rating,
            categories=video.categories,
            genres=video.genres,
            cast_members=video.cast_members,
        )
