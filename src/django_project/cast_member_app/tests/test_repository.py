from uuid import uuid4
import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberModel


@pytest.mark.django_db
class TestDjangoORMCastMemberRepository:
    @pytest.fixture
    def cast_member_model(self):
        return CastMemberModel

    def test_can_save_cast_member_in_database(self, cast_member_model):
        repository = DjangoORMCastMemberRepository(cast_member_model=cast_member_model)
        cast_member = CastMember(
            name="Actor",
            type=CastMemberType.DIRECTOR,
        )
        saved_cast_member = repository.save(cast_member)
        assert saved_cast_member.id is not None
        assert saved_cast_member.id == cast_member.id
        assert saved_cast_member.name == cast_member.name
        assert saved_cast_member.type == cast_member.type

    def test_can_get_cast_member_by_id(self, cast_member_model):
        repository = DjangoORMCastMemberRepository(cast_member_model=cast_member_model)
        cast_member = CastMember(
            name="Actor",
            type=CastMemberType.DIRECTOR,
        )
        retrieved_cast_member = repository.get_by_id(cast_member.id)
        if retrieved_cast_member:
            assert retrieved_cast_member.id == cast_member.id
            assert retrieved_cast_member.name == cast_member.name
            assert retrieved_cast_member.type == cast_member.type

    def test_cast_member_not_found_by_id(self, cast_member_model):
        repository = DjangoORMCastMemberRepository(cast_member_model=cast_member_model)
        retrieved_cast_member = repository.get_by_id(uuid4())
        assert retrieved_cast_member is None
