import re
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
)
from src.core.cast_member.application.use_cases.exceptions import (
    InvalidCastMemberDataException,
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


class TestCreateCastMember(CommonFixtures):
    def test_create_cast_member_successfully(
        self,
        cast_member_repository,
        cast_member_actor,
    ):
        cast_member_repository.save.return_value = CastMember(
            id=cast_member_actor.id,
            name=cast_member_actor.name,
            type=cast_member_actor.type,
        )
        use_case = CreateCastMember(repository=cast_member_repository)
        input = CreateCastMember.Input(
            name=cast_member_actor.name,
            type=cast_member_actor.type,
        )
        output = use_case.execute(input)
        assert output == CreateCastMember.Output(
            id=cast_member_actor.id,
            name=cast_member_actor.name,
            type=cast_member_actor.type,
        )
        assert output.id is not None
        cast_member_repository.save.assert_called_once()

    def test_create_cast_member_with_invalid_name(
        self,
        cast_member_repository,
        cast_member_actor,
    ):
        use_case = CreateCastMember(repository=cast_member_repository)
        input = CreateCastMember.Input(
            name="",
            type=cast_member_actor.type,
        )
        with pytest.raises(
            InvalidCastMemberDataException, match="Name cannot be empty"
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
