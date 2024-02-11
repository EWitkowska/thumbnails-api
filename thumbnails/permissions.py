from rest_framework import permissions


class CanGenerateImages(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.account_type is not None:
            return True
        else:
            return False


class CanGenerateExpiringLink(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.account_type is not None:
            return request.user.account_type.can_generate_expiring_link
        else:
            return False
