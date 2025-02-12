from uuid import uuid4
from django.db import models

from src.core.cast_member.domain.cast_member import CastMemberType


# Create your models here.
class CastMember(models.Model):
    app_label = "cast_member_app"
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=255,
        choices=[
            (member_type.value, member_type.value) for member_type in CastMemberType
        ],
    )

    class Meta:
        db_table = "cast_member"
        verbose_name_plural = "Cast Members"
        verbose_name = "Cast Member"

    def __str__(self):
        return f"name: {self.name} | type: {self.type}"
