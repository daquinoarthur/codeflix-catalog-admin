from rest_framework import status, viewsets
from rest_framework.views import Request, Response

from src.core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from src.core.video.application.use_cases.exceptions import (
    InvalidVideoDataException,
    RelatedEntitiesNotFoundException,
)
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.video_app.serializers import (
    CreateVideoWithoutMediaRequestSerializer,
    CreateVideoWithoutMediaResponseSerializer,
)


class VideoViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        request_serializer = CreateVideoWithoutMediaRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        repository = DjangoORMVideoRepository()
        category_repository = DjangoORMCategoryRepository()
        genre_repository = DjangoORMGenreRepository()
        cast_member_repository = DjangoORMCastMemberRepository()
        use_case = CreateVideoWithoutMedia(
            repository=repository,
            category_repository=category_repository,
            genre_repository=genre_repository,
            cast_member_repository=cast_member_repository,
        )
        input = CreateVideoWithoutMedia.Input(**request_serializer.validated_data)
        try:
            output = use_case.execute(input)
            response_serializer = CreateVideoWithoutMediaResponseSerializer(
                instance=output
            )
        except (RelatedEntitiesNotFoundException, InvalidVideoDataException) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
