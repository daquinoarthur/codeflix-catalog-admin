from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.views import Request, Response

from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
)
from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFoundException,
    InvalidCastMemberDataException,
)
from src.core.cast_member.application.use_cases.list_cast_members import ListCastMember
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
)
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
)
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberRequestSerializer,
    CreateCastMemberResponseSerializer,
    DeleteCastMemberRequestSerializer,
    DeleteCastMemberResponseSerializer,
    ListCastMemberResponseSerializer,
    PartialUpdateCastMemberRequestSerializer,
    PartialUpdateCastMemberResponseSerializer,
    UpdateCastMemberRequestSerializer,
    UpdateCastMemberResponseSerializer,
)


# Create your views here.
class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        repository = DjangoORMCastMemberRepository()
        use_case = ListCastMember(repository=repository)
        input = ListCastMember.Input()
        output = use_case.execute(input)
        response_serializer = ListCastMemberResponseSerializer(output)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        repository = DjangoORMCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        request_serializer = CreateCastMemberRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        input = CreateCastMember.Input(**request_serializer.validated_data)
        try:
            output = use_case.execute(input)
        except InvalidCastMemberDataException as err:
            return Response(
                data={"error": str(err)}, status=status.HTTP_400_BAD_REQUEST
            )
        response_serializer = CreateCastMemberResponseSerializer(instance=output)
        return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk: UUID) -> Response:
        request_serializers = UpdateCastMemberRequestSerializer(
            data={**request.data, "id": pk}
        )
        request_serializers.is_valid(raise_exception=True)
        repository = DjangoORMCastMemberRepository()
        use_case = UpdateCastMember(repository=repository)
        input = UpdateCastMember.Input(**request_serializers.validated_data)
        try:
            output = use_case.execute(input)
            response_serializer = UpdateCastMemberResponseSerializer(instance=output)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except InvalidCastMemberDataException as err:
            return Response(
                data={"error": str(err)}, status=status.HTTP_400_BAD_REQUEST
            )
        except CastMemberNotFoundException as err:
            return Response(data={"error": str(err)}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request: Request, pk: UUID) -> Response:
        request_serializers = PartialUpdateCastMemberRequestSerializer(
            data={**request.data, "id": pk}
        )
        request_serializers.is_valid(raise_exception=True)
        repository = DjangoORMCastMemberRepository()
        use_case = UpdateCastMember(repository=repository)
        input = UpdateCastMember.Input(**request_serializers.validated_data)
        try:
            output = use_case.execute(input)
            response_serializer = PartialUpdateCastMemberResponseSerializer(
                instance=output
            )
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except InvalidCastMemberDataException as err:
            return Response(
                data={"error": str(err)}, status=status.HTTP_400_BAD_REQUEST
            )
        except CastMemberNotFoundException as err:
            return Response(data={"error": str(err)}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request: Request, pk: UUID) -> Response:
        request_serializer = DeleteCastMemberRequestSerializer(data={"id": pk})
        request_serializer.is_valid(raise_exception=True)
        repository = DjangoORMCastMemberRepository()
        use_case = DeleteCastMember(repository=repository)
        input = DeleteCastMember.Input(**request_serializer.validated_data)
        try:
            output = use_case.execute(input)
            response_serializer = DeleteCastMemberResponseSerializer(instance=output)
            return Response(
                data=response_serializer.data, status=status.HTTP_204_NO_CONTENT
            )
        except CastMemberNotFoundException as err:
            return Response(data={"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
