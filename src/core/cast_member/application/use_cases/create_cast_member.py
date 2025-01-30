from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import (
    InvalidCastMemberDataException,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


@dataclass
class CreateCastMember:
    @dataclass
    class Input:
        name: str
        type: CastMemberType

    @dataclass
    class Output:
        id: UUID
        name: str
        type: CastMemberType

    def __init__(self, repository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        try:
            cast_member = CastMember(
                name=input.name,
                type=input.type,
            )
        except (ValueError, TypeError) as e:
            raise InvalidCastMemberDataException(str(e)) from e
        created_cast_member = self.repository.save(cast_member)
        return self.Output(
            id=created_cast_member.id,
            name=created_cast_member.name,
            type=created_cast_member.type,
        )
