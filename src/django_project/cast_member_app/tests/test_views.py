import pytest
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.mark.django_db
class CommonTestFixtures:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def cast_member_repository(self):
        return DjangoORMCastMemberRepository()

    @pytest.fixture
    def create_cast_member(self, cast_member_repository: CastMemberRepository):
        return lambda name, type: cast_member_repository.save(
            CastMember(name=name, type=type)
        )


class TestListCastMembersView(CommonTestFixtures):
    def test_list_cast_members(
        self,
        cast_member_repository,
        create_cast_member,
        client,
    ):
        cast_member_actor = create_cast_member("Actor", CastMemberType.ACTOR)
        cast_member_director = create_cast_member("Director", CastMemberType.DIRECTOR)
        cast_member_path = "/api/cast-members/"
        expected_response = {
            "data": [
                {
                    "id": str(cast_member_actor.id),
                    "name": cast_member_actor.name,
                    "type": cast_member_actor.type.value,
                },
                {
                    "id": str(cast_member_director.id),
                    "name": cast_member_director.name,
                    "type": cast_member_director.type.value,
                },
            ]
        }
        response = client.get(cast_member_path)
        assert response.data == expected_response
        assert response.status_code == 200
        assert len(response.data["data"]) == 2

    def test_list_cast_members_empty(self, client):
        cast_member_path = "/api/cast-members/"
        expected_response = {"data": []}
        response = client.get(cast_member_path)
        assert response.data == expected_response
        assert response.status_code == 200
        assert len(response.data["data"]) == 0
