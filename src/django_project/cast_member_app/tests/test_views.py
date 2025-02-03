import pytest
from rest_framework.test import APIClient
from rest_framework.fields import ErrorDetail
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


class TestCastMemberViewSetListAPI(CommonTestFixtures):
    def test_list_cast_members(
        self,
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


class TestCastMemberViewSetCreateAPI(CommonTestFixtures):
    def test_create_cast_member(self, cast_member_repository, client):
        cast_member_path = "/api/cast-members/"
        payload = {
            "name": "Actor",
            "type": "ACTOR",
        }
        response = client.post(cast_member_path, payload, format="json")
        created_cast_member_actor = cast_member_repository.list()[0]
        expected_response = {
            "id": str(created_cast_member_actor.id),
            "name": created_cast_member_actor.name,
            "type": created_cast_member_actor.type.value,
        }
        assert len(cast_member_repository.list()) == 1
        assert response.data == expected_response

    def test_create_cast_member_with_invalid_name_field(self, client):
        cast_member_path = "/api/cast-members/"
        payload = {
            "name": "",
            "type": "ACTOR",
        }
        response = client.post(cast_member_path, payload, format="json")
        assert response.data == {
            "name": [ErrorDetail(string="This field may not be blank.", code="blank")]
        }

    def test_create_cast_member_with_invalid_type_field(self, client):
        cast_member_path = "/api/cast-members/"
        payload = {
            "name": "Actor",
            "type": "INVALID",
        }
        response = client.post(cast_member_path, payload, format="json")
        assert response.data == {
            "type": [
                ErrorDetail(
                    string='"INVALID" is not a valid choice.', code="invalid_choice"
                )
            ]
        }
