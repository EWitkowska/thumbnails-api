from rest_framework import serializers

from .models import Image, ExpiringLink


class ListImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "url"]
        extra_kwargs = {"url": {"view_name": "image-detail"}}


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["user", "image", "thumbnails"]
        read_only_fields = ["user", "thumbnails"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user

        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        can_retrieve_original_image = (
            instance.user.account_type.can_retrieve_original_image
        )

        if can_retrieve_original_image:
            representation["image"] = instance.image.url
        else:
            representation["image"] = (
                "You don't have permission to retrieve this image."
            )

        return representation


class ListExpiringLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ["id", "url"]
        extra_kwargs = {"url": {"view_name": "expiring-link-detail"}}


class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ["user", "image", "temporary_link", "expires_in"]
        read_only_fields = ["user", "temporary_link"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request is not None:
            self.fields["image"].queryset = Image.objects.filter(user=request.user)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user

        return super().create(validated_data)
