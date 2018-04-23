from rest_framework import serializers


class NotebookViewSerializer(serializers.Serializer):
    url = serializers.URLField()
    images_url = serializers.URLField(required=False)
    start = serializers.CharField(required=False)
    end = serializers.CharField(required=False)

    def validate_images_url(self, value):
        if not value.endswith('/'):
            raise serializers.ValidationError("Image Root URL must end with a '/'")
        return value
