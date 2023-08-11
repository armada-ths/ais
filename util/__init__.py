from rest_framework import serializers


# Allow for setting and array through JSON.
# Without this update function ListSerializer
# will complain that update is not defined.
class ChildSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        return instance


def update_field(
    instance, validated_data, field: str, Serializer: serializers.Serializer
):
    item = validated_data.pop(field, None)
    if item != None:
        serializer = Serializer(getattr(instance, field), data=item, partial=True)

        if serializer.is_valid():
            serializer.save()
