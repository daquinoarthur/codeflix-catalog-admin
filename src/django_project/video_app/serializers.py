from rest_framework import serializers


class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class CategoriesSetField(SetField): ...


class GenresSetField(SetField): ...


class CastMembersSetField(SetField): ...


class CreateVideoWithoutMediaRequestSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    duration = serializers.IntegerField()
    rating = serializers.FloatField()
    categories = CategoriesSetField(child=serializers.UUIDField())
    genres = GenresSetField(child=serializers.UUIDField())
    cast_members = CastMembersSetField(child=serializers.UUIDField())


class CreateVideoWithoutMediaResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    duration = serializers.IntegerField()
    rating = serializers.FloatField()
    categories = CategoriesSetField(child=serializers.UUIDField())
    genres = GenresSetField(child=serializers.UUIDField())
    cast_members = CastMembersSetField(child=serializers.UUIDField())
