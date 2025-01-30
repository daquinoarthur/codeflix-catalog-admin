import re
from uuid import UUID

import pytest

from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
)
from src.core.cast_member.application.use_cases.exceptions import (
    InvalidCastMemberDataException,
)
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class CommonFixtures:
    @pytest.fixture
    def cast_member_repository(self):
        return InMemoryCastMemberRepository()


class TestCreateCastMember(CommonFixtures):
    def test_create_cast_member_successfully(
        self,
        cast_member_repository,
    ):
        use_case = CreateCastMember(repository=cast_member_repository)
        input = CreateCastMember.Input(
            name="Actor",
            type=CastMemberType.ACTOR,
        )
        output = use_case.execute(input)
        assert output.id is not None
        assert output.name == "Actor"
        assert isinstance(output.id, UUID)
        assert isinstance(output.type, CastMemberType)

    def test_create_cast_member_with_invalid_name(
        self,
        cast_member_repository,
    ):
        use_case = CreateCastMember(repository=cast_member_repository)
        input = CreateCastMember.Input(
            name="",
            type=CastMemberType.ACTOR,
        )
        with pytest.raises(
            InvalidCastMemberDataException, match="Name cannot be empty"
        ):
            use_case.execute(input)

    def test_create_cast_member_with_name_greater_than_100_characters(
        self,
        cast_member_repository,
    ):
        use_case = CreateCastMember(repository=cast_member_repository)
        input = CreateCastMember.Input(
            name="a" * 101,
            type=CastMemberType.ACTOR,
        )
        with pytest.raises(
            InvalidCastMemberDataException,
            match="Name cannot be longer than 100 characters",
        ):
            use_case.execute(input)

    def test_create_cast_member_with_invalid_type(self, cast_member_repository):
        use_case = CreateCastMember(repository=cast_member_repository)
        input = CreateCastMember.Input(
            name="John Doe Actor",
            type="invalid_type",
        )
        error_message = "unsupported operand type(s) for 'in': 'str' and 'EnumType'"
        with pytest.raises(
            InvalidCastMemberDataException,
            match=re.escape(error_message),
        ):
            use_case.execute(input)

    def test_create_cast_member_with_invalid_name_and_type(
        self, cast_member_repository
    ):
        use_case = CreateCastMember(repository=cast_member_repository)
        input = CreateCastMember.Input(
            name="",
            type="invalid_type",
        )
        error_message = "Name cannot be empty"
        with pytest.raises(
            InvalidCastMemberDataException,
            match=re.escape(error_message),
        ):
            use_case.execute(input)
