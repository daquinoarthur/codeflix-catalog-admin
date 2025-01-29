import re
import uuid
import pytest
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestCastMemberCreation:
    def test_cast_member_creation_with_valid_values(self):
        cast_member = CastMember(name="Actor", type=CastMemberType.ACTOR)
        assert cast_member.name == "Actor"
        assert cast_member.type == CastMemberType.ACTOR

    def test_cast_member_creation_raises_value_error_with_empty_name(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            CastMember(name="", type=CastMemberType.ACTOR)

    def test_cast_member_creation_raises_value_error_name_greater_than_100_characters(
        self,
    ):
        with pytest.raises(
            ValueError, match="Name cannot be longer than 100 characters"
        ):
            CastMember(name=200 * "a", type=CastMemberType.ACTOR)

    def test_cast_member_instance_is_created_with_uuid_by_default_if_not_passed(self):
        cast_member = CastMember(name="Actor", type=CastMemberType.ACTOR)
        assert cast_member.id is not None
        assert isinstance(cast_member.id, uuid.UUID)

    def test_cast_member_creation_raises_value_error_with_invalid_type(self):
        error_message = "unsupported operand type(s) for 'in': 'str' and 'EnumType'"
        with pytest.raises(
            TypeError,
            match=re.escape(error_message),
        ):
            CastMember(name="Actor", type="INVALID")

    def test_cast_member_str_method(self):
        cast_member = CastMember(name="Actor", type=CastMemberType.ACTOR)
        assert str(cast_member) == "CastMember - name: Actor | type: (ACTOR)"

    def test_cast_member_repr_method(self):
        cast_member = CastMember(name="Actor", type=CastMemberType.ACTOR)
        assert repr(cast_member) == "<CastMember - name: Actor | type: (ACTOR)>"

    def test_cast_member_eq_method(self):
        common_id = uuid.uuid4()
        cast_member = CastMember(id=common_id, name="Actor", type=CastMemberType.ACTOR)
        cast_member_2 = CastMember(
            id=common_id, name="Actor", type=CastMemberType.ACTOR
        )
        cast_member_3 = CastMember(name="Actor", type=CastMemberType.ACTOR)
        assert cast_member == cast_member_2
        assert cast_member != cast_member_3


class TestCastMemberUpdate:
    def test_cast_member_change_name(self):
        cast_member = CastMember(name="Actor", type=CastMemberType.ACTOR)
        cast_member.change_name("Director")
        assert cast_member.name == "Director"

    def test_cast_member_change_type(self):
        cast_member = CastMember(name="Actor", type=CastMemberType.ACTOR)
        cast_member.change_type(CastMemberType.DIRECTOR)
        assert cast_member.type == CastMemberType.DIRECTOR

    def test_cast_member_change_name_raises_value_error_with_empty_name(self):
        cast_member = CastMember(name="Actor", type=CastMemberType.ACTOR)
        with pytest.raises(ValueError, match="Name cannot be empty"):
            cast_member.change_name("")

    def test_cast_member_change_name_raises_value_error_name_greater_than_100_characters(
        self,
    ):
        cast_member = CastMember(name="Actor", type=CastMemberType.ACTOR)
        with pytest.raises(
            ValueError, match="Name cannot be longer than 100 characters"
        ):
            cast_member.change_name(200 * "a")

    def test_cast_member_change_type_raises_type_error_with_invalid_type(self):
        cast_member = CastMember(name="Actor", type=CastMemberType.ACTOR)
        error_message = "unsupported operand type(s) for 'in': 'str' and 'EnumType'"
        with pytest.raises(
            TypeError,
            match=re.escape(error_message),
        ):
            cast_member.change_type("INVALID")
