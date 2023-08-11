from rest_framework import serializers


def update_field(
    instance, validated_data, field: str, Serializer: serializers.Serializer
):
    item = validated_data.pop(field, None)
    if item != None:
        serializer = Serializer(getattr(instance, field), data=item, partial=True)

        if serializer.is_valid():
            serializer.save()
