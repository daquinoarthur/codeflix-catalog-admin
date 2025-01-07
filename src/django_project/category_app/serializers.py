from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField(default=True)


class ListCategoryResponseSerializer(serializers.Serializer):
    data = CategorySerializer(many=True)


class RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategorySerializer(source="*")


class CreateCategoryResponseSerializer(serializers.Serializer):
    data = CategorySerializer(source="*")


class UpdateCategoryIdSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField(default=True)


class UpdateCategoryResponseSerializer(serializers.Serializer):
    data = CategorySerializer(source="*")
