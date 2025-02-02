from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberModel


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_member_model: CastMemberModel | None = None):
        self.cast_member_model = cast_member_model or CastMemberModel

    def save(self, cast_member: CastMember) -> CastMember:
        created_cast_member = self.cast_member_model.objects.create(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type.value,
        )
        return CastMember(
            id=created_cast_member.id,
            name=created_cast_member.name,
            type=CastMemberType[created_cast_member.type],
        )

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member = self.cast_member_model.objects.get(id=id)
        except self.cast_member_model.DoesNotExist:
            return None
        return CastMember(
            id=cast_member.id,
            name=cast_member.name,
            type=CastMemberType[cast_member.type],
        )

    def delete(self, id: UUID) -> None:
        self.cast_member_model.objects.filter(id=id).delete()

    def list(self) -> list[CastMember]:
        return [
            CastMember(
                id=cast_member.id,
                name=cast_member.name,
                type=CastMemberType[cast_member.type],
            )
            for cast_member in self.cast_member_model.objects.all()
        ]

    def update(self, cast_member: CastMember) -> CastMember | None:
        try:
            persisted_cast_member = (
                self.cast_member_model.objects.select_for_update().get(
                    id=cast_member.id
                )
            )
            update_fields = {
                "name": cast_member.name,
                "type": cast_member.type.value,
            }
            self.cast_member_model.objects.filter(id=cast_member.id).update(
                **update_fields
            )
            persisted_cast_member.refresh_from_db()
            return CastMember(
                id=persisted_cast_member.id,
                name=persisted_cast_member.name,
                type=CastMemberType[persisted_cast_member.type],
            )
        except self.cast_member_model.DoesNotExist:
            return None
