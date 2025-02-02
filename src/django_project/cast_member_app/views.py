from rest_framework import status, viewsets
from rest_framework.views import Request, Response

from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.core.cast_member.application.use_cases.list_cast_members import (
    ListCastMember,
)
from src.django_project.cast_member_app.serializers import (
    ListCastMemberResponseSerializer,
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
