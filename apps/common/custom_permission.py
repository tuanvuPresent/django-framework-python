from rest_framework import permissions
from django.core.cache import cache
from apps.account.constant import UserType
from apps.account.models import GroupApiPermission


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
        return obj.user_id == request.user.id or request.user.user_type == UserType.ADMIN.value

 
class GenericApiPermission(permissions.BasePermission):
    message = "You do not have permission to perform action"
    permission_code = '{api_view}.{action}'
    CACHE_KEY = 'permissions{user_id}'
    CACHE_TTL = 5 * 60

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True

        perm_code = self.permission_code.format(api_view=view.__class__.__name__.lower(), action=view.action)
        return perm_code in self.get_user_permissions(request.user)

    def get_user_permissions(self, user):
        perms = cache.get(self.CACHE_KEY.format(user_id=user.id))
        if perms:
            return perms

        api_perms = set()
        if hasattr(user, 'userapipermission_set'):
            api_perms = set(user.userapipermission_set.values_list('api_code', flat=True))
        group_api_perms = set(GroupApiPermission.objects.filter(group__user=user.id).values_list('api_code', flat=True))
        perms = {*api_perms, *group_api_perms}
        cache.set(self.CACHE_KEY.format(user_id=user.id), perms, self.CACHE_TTL)
        return perms
