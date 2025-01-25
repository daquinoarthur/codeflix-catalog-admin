from rest_framework import serializers


class GenreSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListGenreResponseSerializer(serializers.Serializer):
    data = GenreSerializer(many=True)


class RetrieveGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class CategoriesSetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class RetrieveGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    categories = CategoriesSetField(child=serializers.UUIDField())


class CreateGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    name = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    categories = CategoriesSetField(child=serializers.UUIDField())


class CreateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class UpdateGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    categories = CategoriesSetField(child=serializers.UUIDField())


class UpdateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    categories = CategoriesSetField(child=serializers.UUIDField())


class PartialUpdateGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100, required=False)
    is_active = serializers.BooleanField(required=False)
    categories = CategoriesSetField(child=serializers.UUIDField(), required=False)


class PartialUpdateGenreResponseSerializer(UpdateGenreResponseSerializer):
    pass


class DeleteGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
