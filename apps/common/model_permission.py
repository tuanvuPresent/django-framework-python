from rest_framework.permissions import BasePermission


class GenericApiViewPermission(BasePermission):
    message = "You do not have permission to perform action"
    permission_code = '{app_label}.{api_view}_{action}'

    def _get_permission(self, action, perm_slug):
        app, api_view = perm_slug.split(".")
        perm = self.permission_code.format(app_label=app, api_view=api_view, action=action)
        return perm

    def has_permission(self, request, view):
        perm = self._get_permission(action=view.action, perm_slug=view.perm_slug)
        if request.user.has_perm(perm):
            return True
        return False
