from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class CastMemberData:
    id: UUID
    name: str
    type: CastMemberType


@dataclass
class ListCastMember:
    @dataclass
    class Input: ...

    @dataclass
    class Output:
        data: list[CastMemberData]

    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        cast_members = self.repository.list()
        return ListCastMember.Output(
            data=[
                CastMemberData(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
                for cast_member in cast_members
            ]
        )
