import uuid


class Category:
    def __init__(
        self,
        name,
        id=None,
        description="",
        is_active=True,
    ):
        self.id = id or uuid.uuid4()
        self.name = name
        self.description = description
        self.is_active = is_active

        if len(self.name) > 255:
            raise ValueError("name must have less than 256 characters")

    def __str__(self):
        is_active = "Yes" if self.is_active else "No"
        return (
            f"Category name: {self.name}"
            f" - Category description: {self.description}"
            f" - Category is active: {is_active}"
        )

    def __repr__(self):
        return f"<Category: {self.name} - id: {self.id}>"
