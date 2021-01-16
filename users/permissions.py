from rest_framework import permissions


class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'


class AdminOrModeratorOrAuthorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin' or
            obj.author or
            request.user.role == 'moderator'
        )
