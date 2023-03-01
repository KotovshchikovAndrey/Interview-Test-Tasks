from rest_framework import permissions


class IsTaskOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        owner = obj.user.id

        if current_user.id != owner:
            return False

        return True
