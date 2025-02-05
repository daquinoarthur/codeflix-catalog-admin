from rest_framework import serializers
from src.core.cast_member.domain.cast_member import CastMemberType


class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [
            (cast_member_type.value, cast_member_type.value)
            for cast_member_type in CastMemberType
        ]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return CastMemberType(super().to_internal_value(data))

    def to_representation(self, value):
        return str(super().to_representation(value))


class CastMemberSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    type = CastMemberTypeField()


class ListCastMemberResponseSerializer(serializers.Serializer):
    data = CastMemberSerializer(many=True)


class CreateCastMemberRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = CastMemberTypeField()


class CreateCastMemberResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    type = CastMemberTypeField()


class UpdateCastMemberRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    type = CastMemberTypeField()


class UpdateCastMemberResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    type = CastMemberTypeField()
