from uuid import uuid4
import pytest

from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFoundException,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class CommonFixtures:
    @pytest.fixture
    def create_cast_member(self):
        return lambda name, type: CastMember(name=name, type=type)

    @pytest.fixture
    def cast_member_actor(self, create_cast_member):
        return create_cast_member("John Doe", type=CastMemberType.ACTOR)

    @pytest.fixture
    def cast_member_director(self, create_cast_member):
        return create_cast_member("Jane Doe", type=CastMemberType.DIRECTOR)

    @pytest.fixture
    def cast_member_repository(self, cast_member_actor, cast_member_director):
        return InMemoryCastMemberRepository(
            cast_members=[cast_member_actor, cast_member_director]
        )

    @pytest.fixture
    def cast_member_repository_empty(self):
        return InMemoryCastMemberRepository()


class TestDeleteCastMember(CommonFixtures):
    def test_delete_cast_member_successfully(
        self,
        cast_member_repository,
        cast_member_actor,
    ):
        use_case = DeleteCastMember(repository=cast_member_repository)
        input = DeleteCastMember.Input(id=cast_member_actor.id)
        assert len(cast_member_repository.list()) == 2
        output = use_case.execute(input)
        assert output == DeleteCastMember.Output(
            detail="Cast member deleted successfully"
        )
        assert len(cast_member_repository.list()) == 1

    def test_delete_cast_member_not_found(self, cast_member_repository_empty):
        use_case = DeleteCastMember(repository=cast_member_repository_empty)
        non_existing_cast_member_id = uuid4()
        input = DeleteCastMember.Input(id=non_existing_cast_member_id)
        with pytest.raises(
            CastMemberNotFoundException,
            match=f"Cast member with id {non_existing_cast_member_id}",
        ):
            use_case.execute(input)
