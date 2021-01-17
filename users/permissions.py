from rest_framework import permissions


class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated and
                (request.user.is_superuser or
                 request.user.role == 'admin')
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


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
