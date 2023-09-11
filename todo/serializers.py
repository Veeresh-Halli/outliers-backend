from rest_framework import serializers


class TaskSerializers(serializers.Serializer):
    title = serializers.RegexField(
        regex=r"^[a-zA-Z0-9\,\.\s]*$", max_length=50, required=True
    )
    description = serializers.RegexField(
        regex=r"^[a-zA-Z0-9\,\.\s]*$", max_length=2000, required=True
    )


class ToggleTaskSerializer(serializers.Serializer):
    completed = serializers.BooleanField(required=True)
