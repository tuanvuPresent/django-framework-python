from rest_framework import permissions

from apps.account.constant import UserType


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser and request.user.is_staff


class IsStaffUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == UserType.STAFF.value


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == UserType.ADMIN.value


class IsCeoUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == UserType.CEO.value


class IsLeaderUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == UserType.LEADER.value


class IsStaffUserObjects(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == UserType.STAFF.value

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user


class IsAdminUserObjects(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == UserType.ADMIN.value

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user


class IsCeoUserObjects(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == UserType.CEO.value

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user


class IsLeaderUserObjects(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == UserType.LEADER.value

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsUserObjects(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user


class IsAdminUserOrIsUserObjects(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if type(obj) == type(request.user):
            return obj == request.user or request.user.user_type == UserType.ADMIN.value
        return obj.user_id == request.user or request.user.user_type == UserType.ADMIN.value
