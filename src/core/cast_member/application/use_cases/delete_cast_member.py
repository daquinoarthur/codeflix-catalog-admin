from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFoundException,
)
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class DeleteCastMember:
    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        detail: str

    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    def execute(self, input) -> Output:
        cast_member = self.repository.get_by_id(input.id)
        if not cast_member:
            raise CastMemberNotFoundException(
                f"Cast member with id {input.id} not found"
            )
        self.repository.delete(input.id)
        return self.Output(detail="Cast member deleted successfully")
