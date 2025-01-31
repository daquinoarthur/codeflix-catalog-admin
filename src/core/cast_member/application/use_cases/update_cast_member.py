from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFoundException,
    InvalidCastMemberDataException,
)
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class UpdateCastMember:
    @dataclass
    class Input:
        id: UUID
        name: str | None = None
        type: CastMemberType | None = None

    @dataclass
    class Output:
        id: UUID
        name: str
        type: CastMemberType

    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output | None:
        cast_member = self.repository.get_by_id(input.id)
        if not cast_member:
            raise CastMemberNotFoundException(
                f"Can not update cast member with id: {input.id}. Cast member not found."
            )
        try:
            cast_member.change_name(input.name) if input.name else None
            cast_member.change_type(input.type) if input.type else None
        except (ValueError, TypeError) as error:
            raise InvalidCastMemberDataException(str(error))
        updated_cast_member = self.repository.update(cast_member)
        return self.Output(
            id=updated_cast_member.id,
            name=updated_cast_member.name,
            type=updated_cast_member.type,
        )
