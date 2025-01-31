import re
from unittest.mock import create_autospec
import pytest

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFoundException,
    InvalidCastMemberDataException,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class CommonFixtures:
    @pytest.fixture
    def cast_member_repository(self):
        return create_autospec(CastMemberRepository)

    @pytest.fixture
    def create_cast_member(self):
        return lambda name, type: CastMember(name=name, type=type)

    @pytest.fixture
    def cast_member_actor(self, create_cast_member):
        return create_cast_member("John Doe", type=CastMemberType.ACTOR)

    @pytest.fixture
    def cast_member_repository_with_instances_created(
        self,
        cast_member_repository,
        cast_member_actor,
    ):
        cast_member_repository.get_by_id.return_value = cast_member_actor
        return cast_member_repository


class TestUpdateCastMember(CommonFixtures):
    def test_update_cast_member_successfully(
        self,
        cast_member_repository_with_instances_created,
        cast_member_actor,
    ):
        cast_member_repository_with_instances_created.update.return_value = CastMember(
            id=cast_member_actor.id,
            name="John Doe Director",
            type=CastMemberType.DIRECTOR,
        )
        use_case = UpdateCastMember(
            repository=cast_member_repository_with_instances_created
        )
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
        cast_member_repository_with_instances_created.update.assert_called_once_with(
            cast_member_actor
        )

    def test_update_cast_member_only_name(
        self,
        cast_member_repository_with_instances_created,
        cast_member_actor,
    ):
        cast_member_repository_with_instances_created.update.return_value = CastMember(
            id=cast_member_actor.id,
            name="John Doe Updated",
            type=CastMemberType.ACTOR,
        )
        use_case = UpdateCastMember(
            repository=cast_member_repository_with_instances_created
        )
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
        cast_member_repository_with_instances_created,
        cast_member_actor,
    ):
        cast_member_repository_with_instances_created.update.return_value = CastMember(
            id=cast_member_actor.id,
            name="John Doe",
            type=CastMemberType.DIRECTOR,
        )
        use_case = UpdateCastMember(
            repository=cast_member_repository_with_instances_created
        )
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
        cast_member_repository_with_instances_created,
        cast_member_actor,
    ):
        cast_member_repository_with_instances_created.get_by_id.return_value = None
        use_case = UpdateCastMember(
            repository=cast_member_repository_with_instances_created
        )
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
        cast_member_repository_with_instances_created,
        cast_member_actor,
    ):
        use_case = UpdateCastMember(
            repository=cast_member_repository_with_instances_created
        )
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
        cast_member_repository_with_instances_created,
        cast_member_actor,
    ):
        use_case = UpdateCastMember(
            repository=cast_member_repository_with_instances_created
        )
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
