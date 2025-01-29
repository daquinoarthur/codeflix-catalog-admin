from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4


class CastMemberType(Enum):
    DIRECTOR = "DIRECTOR"
    ACTOR = "ACTOR"


@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self._validate()

    def __str__(self):
        return f"CastMember - name: {self.name} | type: ({self.type.value})"

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __eq__(self, other):
        if not isinstance(other, CastMember):
            return False
        return self.id == other.id

    def _validate(self):
        self._validate_name(self.name)
        self._validate_type(self.type)

    def _validate_name(self, name):
        if not name:
            raise ValueError("Name cannot be empty")
        if len(name) > 100:
            raise ValueError("Name cannot be longer than 100 characters")

    def _validate_type(self, type):
        if type not in CastMemberType:
            raise TypeError("Invalid type")

    def change_name(self, name):
        self._validate_name(name)
        self.name = name

    def change_type(self, type):
        self._validate_type(type)
        self.type = type
