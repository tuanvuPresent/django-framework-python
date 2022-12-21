from rest_framework.permissions import BasePermission


class GenericApiViewPermission(BasePermission):
    APP_LABEL = 'apps'
    message = 'You do not have permission to perform action'
    permission_code = '{app_label}.{func}_{action}'

    def _get_permission(self, action, func):
        perm = self.permission_code.format(app_label=self.APP_LABEL, func=func, action=action)
        return perm

    def has_permission(self, request, view):
        perm = self._get_permission(action=view.action, func=resolve(request.path)._func_path)
        if request.user.has_perm(perm):
            return True
        return False
