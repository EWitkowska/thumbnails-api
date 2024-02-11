from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    ListImageSerializer,
    ImageSerializer,
    ListExpiringLinkSerializer,
    ExpiringLinkSerializer,
)
from .models import Image, ExpiringLink
from .permissions import CanGenerateImages, CanGenerateExpiringLink


class ImageViewSet(ModelViewSet):
    """

    Note: For Basic Authentication, please use your email as the username.

    """

    queryset = Image.objects.all().order_by("id")
    permission_classes = [IsAuthenticated, CanGenerateImages]
    http_method_names = ["get", "post", "options", "head"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListImageSerializer
        return ImageSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ExpiringLinkViewSet(ModelViewSet):
    """

    Note: For Basic Authentication, please use your email as the username.

    """

    queryset = ExpiringLink.objects.all().order_by("id")
    permission_classes = [IsAuthenticated, CanGenerateExpiringLink]
    http_method_names = ["get", "post", "options", "head"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListExpiringLinkSerializer
        return ExpiringLinkSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
