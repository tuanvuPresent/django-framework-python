from rest_framework import permissions

from apps.account.constant import STAFF, ADMIN, CEO, LEADER


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser and request.user.is_staff


class IsStaffUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == STAFF


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == ADMIN


class IsCeoUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == CEO


class IsLeaderUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == LEADER


class IsStaffUserObjects(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == STAFF

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user


class IsAdminUserObjects(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == ADMIN

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user


class IsCeoUserObjects(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == CEO

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user


class IsLeaderUserObjects(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == LEADER

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
            return obj == request.user or request.user.user_type == ADMIN
        return obj.user_id == request.user or request.user.user_type == ADMIN
