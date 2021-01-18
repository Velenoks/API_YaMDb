from rest_framework import permissions


class IsModerOrAuthorOrReadOnly(permissions.BasePermission):
    """Проверка на Автора и Модератора."""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or 'moderator' == request.user.role
                or obj.author == request.user)


class IsAdmin(permissions.BasePermission):
    """Проверка на Админа."""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_superuser and
                request.user.is_authenticated)