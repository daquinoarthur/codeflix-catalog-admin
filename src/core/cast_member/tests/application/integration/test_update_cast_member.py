import re

import pytest

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFoundException,
    InvalidCastMemberDataException,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
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
    def cast_member_repository(self, cast_member_actor):
        return InMemoryCastMemberRepository(cast_members=[cast_member_actor])

    @pytest.fixture
    def cast_member_repository_empty(self):
        return InMemoryCastMemberRepository()


class TestUpdateCastMember(CommonFixtures):
    def test_update_cast_member_successfully(
        self,
        cast_member_repository,
        cast_member_actor,
    ):
        use_case = UpdateCastMember(repository=cast_member_repository)
        input = UpdateCastMember.Input(
            id=cast_member_actor.id,
            name="John Doe Director",
            type=CastMemberType.DIRECTOR,
        )
        output = use_case.execute(input)
        assert output == UpdateCastMember.Output(
            id=cast_member_actor.id,
            name="John Doe Director",
            type=cast_member_actor.type,
        )

    def test_update_cast_member_only_name(
        self,
        cast_member_repository,
        cast_member_actor,
    ):
        use_case = UpdateCastMember(repository=cast_member_repository)
        input = UpdateCastMember.Input(
            id=cast_member_actor.id,
            name="John Doe Updated",
        )
        output = use_case.execute(input)
        assert output == UpdateCastMember.Output(
            id=cast_member_actor.id,
            name="John Doe Updated",
            type=cast_member_actor.type,
        )

    def test_update_cast_member_only_type(
        self,
        cast_member_repository,
        cast_member_actor,
    ):
        use_case = UpdateCastMember(repository=cast_member_repository)
        input = UpdateCastMember.Input(
            id=cast_member_actor.id,
            type=CastMemberType.DIRECTOR,
        )
        output = use_case.execute(input)
        assert output == UpdateCastMember.Output(
            id=cast_member_actor.id,
            name=cast_member_actor.name,
            type=CastMemberType.DIRECTOR,
        )

    def test_update_cast_member_not_found(
        self,
        cast_member_repository_empty,
        cast_member_actor,
    ):
        use_case = UpdateCastMember(repository=cast_member_repository_empty)
        input = UpdateCastMember.Input(
            id=cast_member_actor.id,
            name="John Doe Updated",
        )
        with pytest.raises(
            CastMemberNotFoundException,
            match=f"Can not update cast member with id: {cast_member_actor.id}. Cast member not found.",
        ):
            use_case.execute(input)

    def test_update_cast_member_name_is_to_long(
        self,
        cast_member_repository,
        cast_member_actor,
    ):
        use_case = UpdateCastMember(repository=cast_member_repository)
        input = UpdateCastMember.Input(
            id=cast_member_actor.id,
            name="a" * 101,
        )
        error_message = "Name cannot be longer than 100 characters"
        with pytest.raises(
            InvalidCastMemberDataException,
            match=error_message,
        ):
            use_case.execute(input)

    def test_update_cast_member_invalid_type(
        self,
        cast_member_repository,
        cast_member_actor,
    ):
        use_case = UpdateCastMember(repository=cast_member_repository)
        input = UpdateCastMember.Input(
            id=cast_member_actor.id,
            type="invalid",
        )
        error_message = "unsupported operand type(s) for 'in': 'str' and 'EnumType'"
        with pytest.raises(
            InvalidCastMemberDataException,
            match=re.escape(error_message),
        ):
            use_case.execute(input)
