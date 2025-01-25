from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Genre:
    name: str
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)
    categories: set[UUID] = field(default_factory=set)

    def __post_init__(self):
        self._validate()

    def __str__(self):
        return f"Genre: {self.name} - Is Active: {'Yes' if self.is_active else 'No'} - id: {self.id}"

    def __repr__(self):
        return f"<Genre: {self.name} - id: {self.id}>"

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return self.id == other.id

    def change_name(self, name):
        self.name = name
        self._validate()

    def _validate(self):
        self._validate_name()

    def _validate_name(self):
        if not self.name:
            raise ValueError("Name cannot be empty.")
        if len(self.name) > 255:
            raise ValueError("Name cannot be longer than 255 characters.")

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def add_category(self, category_id: UUID):
        self.categories.add(category_id)

    def remove_category(self, category_id: UUID):
        self.categories.remove(category_id)
