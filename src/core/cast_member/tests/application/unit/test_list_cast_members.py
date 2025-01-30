from unittest.mock import create_autospec
import pytest

from src.core.cast_member.application.use_cases.list_cast_members import (
    CastMemberData,
    ListCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class CommonFixtures:
    @pytest.fixture
    def cast_member_repository(self):
        return create_autospec(CastMemberRepository)

    @pytest.fixture
    def create_cast_member(self):
        return lambda name, type: CastMember(
            name=name,
            type=type,
        )

    @pytest.fixture
    def cast_member_actor(self, create_cast_member):
        return create_cast_member("John Doe Actor", type=CastMemberType.ACTOR)

    @pytest.fixture
    def cast_member_director(self, create_cast_member):
        return create_cast_member("Jane Doe Director", type=CastMemberType.DIRECTOR)

    @pytest.fixture
    def cast_member_repository_with_instances_created(
        self,
        cast_member_repository,
        cast_member_actor,
        cast_member_director,
    ):
        cast_member_repository.list.return_value = [
            cast_member_actor,
            cast_member_director,
        ]
        return cast_member_repository

    @pytest.fixture
    def cast_member_repository_empty(self, cast_member_repository):
        cast_member_repository.list.return_value = []
        return cast_member_repository


class TestListCastMembers(CommonFixtures):
    def test_list_cast_members_successfully(
        self,
        cast_member_repository_with_instances_created,
        cast_member_actor,
        cast_member_director,
    ):
        use_case = ListCastMember(
            repository=cast_member_repository_with_instances_created
        )
        input = ListCastMember.Input()
        output = use_case.execute(input)
        assert output == ListCastMember.Output(
            data=[
                CastMemberData(
                    id=cast_member_actor.id,
                    name=cast_member_actor.name,
                    type=cast_member_actor.type,
                ),
                CastMemberData(
                    id=cast_member_director.id,
                    name=cast_member_director.name,
                    type=cast_member_director.type,
                ),
            ]
        )

    def test_list_cast_members_empty_list(
        self,
        cast_member_repository_empty,
    ):
        use_case = ListCastMember(repository=cast_member_repository_empty)
        input = ListCastMember.Input()
        output = use_case.execute(input)
        assert output == ListCastMember.Output(data=[])
