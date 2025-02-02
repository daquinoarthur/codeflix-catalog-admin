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

    def test_can_delete_a_cast_member_record(self, cast_member_model):
        repository = DjangoORMCastMemberRepository(cast_member_model=cast_member_model)
        cast_member_1 = CastMember(
            name="Actor",
            type=CastMemberType.ACTOR,
        )
        cast_member_2 = CastMember(
            name="Director",
            type=CastMemberType.DIRECTOR,
        )
        cast_member_3 = CastMember(
            name="Actor",
            type=CastMemberType.ACTOR,
        )
        repository.save(cast_member_1)
        repository.save(cast_member_2)
        repository.save(cast_member_3)
        assert len(repository.list()) == 3

    def test_cast_member_not_found_when_deleting(self, cast_member_model):
        repository = DjangoORMCastMemberRepository(cast_member_model=cast_member_model)
        cast_member = CastMember(
            name="Actor",
            type=CastMemberType.ACTOR,
        )
        repository.save(cast_member)
        repository.delete(uuid4())
        assert len(repository.list()) == 1

    def test_can_list_cast_members(self, cast_member_model):
        repository = DjangoORMCastMemberRepository(cast_member_model=cast_member_model)
        cast_member_1 = CastMember(
            name="Actor",
            type=CastMemberType.ACTOR,
        )
        cast_member_2 = CastMember(
            name="Director",
            type=CastMemberType.DIRECTOR,
        )
        cast_member_3 = CastMember(
            name="Actor",
            type=CastMemberType.ACTOR,
        )
        repository.save(cast_member_1)
        repository.save(cast_member_2)
        repository.save(cast_member_3)
        assert len(repository.list()) == 3
        persisted_cast_member_1 = repository.get_by_id(cast_member_1.id)
        assert persisted_cast_member_1 is not None
        assert persisted_cast_member_1.id == cast_member_1.id
        assert persisted_cast_member_1.name == cast_member_1.name
        assert persisted_cast_member_1.type == cast_member_1.type
        persisted_cast_member_2 = repository.get_by_id(cast_member_2.id)
        assert persisted_cast_member_2 is not None
        assert persisted_cast_member_2.id == cast_member_2.id
        assert persisted_cast_member_2.name == cast_member_2.name
        assert persisted_cast_member_2.type == cast_member_2.type
        persisted_cast_member_3 = repository.get_by_id(cast_member_3.id)
        assert persisted_cast_member_3 is not None
        assert persisted_cast_member_3.id == cast_member_3.id
        assert persisted_cast_member_3.name == cast_member_3.name
        assert persisted_cast_member_3.type == cast_member_3.type

    def test_can_update_cast_member(self, cast_member_model):
        repository = DjangoORMCastMemberRepository(cast_member_model=cast_member_model)
        cast_member = CastMember(
            name="Actor",
            type=CastMemberType.ACTOR,
        )
        repository.save(cast_member)
        cast_member.name = "Director"
        cast_member.type = CastMemberType.DIRECTOR
        updated_cast_member = repository.update(cast_member)
        assert updated_cast_member is not None
        assert updated_cast_member.id == cast_member.id
        assert updated_cast_member.name == cast_member.name
        assert updated_cast_member.type == cast_member.type
