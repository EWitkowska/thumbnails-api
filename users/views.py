from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import UserSerializer, AccountSerializer
from .models import Account

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put", "options", "head"]

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        self.object = self.get_object()

        return self.update(request, *args, **kwargs)


class AccountViewSet(ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [IsAdminUser]
