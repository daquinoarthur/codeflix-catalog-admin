from uuid import UUID

from rest_framework import viewsets
from rest_framework.views import Request, Response, status

from src.core.category.application.use_cases.exceptions import CategoryNotFoundException
from src.core.genre.application.exceptions import (
    GenreNotFoundException,
    InvalidGenreDataException,
    RelatedCategoriesNotFoundException,
)
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.get_genre import GetGenre
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import (
    CreateGenreRequestSerializer,
    CreateGenreResponseSerializer,
    DeleteGenreRequestSerializer,
    ListGenreResponseSerializer,
    PartialUpdateGenreRequestSerializer,
    PartialUpdateGenreResponseSerializer,
    RetrieveGenreRequestSerializer,
    RetrieveGenreResponseSerializer,
    UpdateGenreRequestSerializer,
    UpdateGenreResponseSerializer,
)


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        genre_repository = DjangoORMGenreRepository()
        use_case = ListGenre(repository=genre_repository)
        input = ListGenre.Input()
        output = use_case.execute(input)
        response_serializer = ListGenreResponseSerializer(output)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        request_serializer = CreateGenreRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        use_case = CreateGenre(
            genre_repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )
        input = CreateGenre.Input(
            name=request_serializer.validated_data["name"],
            category_ids=set(request_serializer.validated_data["categories"]),
            is_active=request_serializer.validated_data["is_active"],
        )
        try:
            output = use_case.execute(input)
        except (InvalidGenreDataException, RelatedCategoriesNotFoundException) as err:
            return Response(
                data={"error": str(err)}, status=status.HTTP_400_BAD_REQUEST
            )

        response_serializer = CreateGenreResponseSerializer(instance=output)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        request_serializer = RetrieveGenreRequestSerializer(data={"id": pk})
        request_serializer.is_valid(raise_exception=True)
        repository = DjangoORMGenreRepository()
        use_case = GetGenre(repository=repository)
        input = GetGenre.Input(**request_serializer.validated_data)
        try:
            output = use_case.execute(input)
        except GenreNotFoundException as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        response_serializer = RetrieveGenreResponseSerializer(instance=output.data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk: UUID | None = None):
        request_serializer = UpdateGenreRequestSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        request_serializer.is_valid(raise_exception=True)
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()
        use_case = UpdateGenre(
            repository=repository, category_repository=category_repository
        )
        input = UpdateGenre.Input(**request_serializer.validated_data)
        try:
            output = use_case.execute(input)
        except GenreNotFoundException as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        response_serializer = UpdateGenreResponseSerializer(instance=output)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk: UUID | None = None):
        request_serializer = PartialUpdateGenreRequestSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        request_serializer.is_valid(raise_exception=True)
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()
        use_case = UpdateGenre(
            repository=repository, category_repository=category_repository
        )
        input = UpdateGenre.Input(**request_serializer.validated_data)
        try:
            output = use_case.execute(input)
        except (GenreNotFoundException, CategoryNotFoundException) as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        response_serializer = PartialUpdateGenreResponseSerializer(instance=output)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request: Request, pk: UUID | None = None) -> Response:
        request_serializer = DeleteGenreRequestSerializer(data={"id": pk})
        request_serializer.is_valid(raise_exception=True)
        repository = DjangoORMGenreRepository()
        use_case = DeleteGenre(repository=repository)
        input = DeleteGenre.Input(**request_serializer.validated_data)
        try:
            output = use_case.execute(input)
        except GenreNotFoundException as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"detail": output.detail},
            status=status.HTTP_200_OK,
        )
