from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_members=None):
        self.cast_members = cast_members or []

    def save(self, cast_member):
        self.cast_members.append(cast_member)
        return cast_member

    def get_by_id(self, id):
        return next(
            (cast_member for cast_member in self.cast_members if cast_member.id == id),
            None,
        )

    def delete(self, id):
        self.cast_members = [
            cast_member for cast_member in self.cast_members if cast_member.id != id
        ]

    def update(self, cast_member):
        self.cast_members.remove(cast_member)
        self.cast_members.append(cast_member)
        return cast_member

    def list(self):
        return [cast_member for cast_member in self.cast_members]
