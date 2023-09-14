from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.action in ("update", "partial_update"):
            return obj == request.user
        if view.action == "destroy":
            return obj == request.user or request.user.is_staff
