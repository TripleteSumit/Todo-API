from rest_framework.permissions import BasePermission


class IsAdminFromModel(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "admin"
