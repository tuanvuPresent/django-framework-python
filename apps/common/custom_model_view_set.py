from apps.common.custom_authentication import JWTAuthentication
from apps.common.serializer import NoneSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import GenericViewSet


class BaseResponse:

    def __init__(self, status=True, code=0, message=None, data=None):
        self.status = status
        self.code = code
        self.message = message
        self.data = {
            'status': self.status,
            'code': self.code,
            'message': self.message,
            'data': data,
        }

        
class AuthenticationMixin:
    authentication_classes_action = {}
   
    def get_authenticators(self):
        method = self.request.method.lower()
        if method == 'options':
            _action = 'metadata'
        else:
            _action = self.action_map.get(method)
        try:
            auth_classes = self.authentication_classes_action[_action]
            return [auth() for auth in auth_classes]
        except (KeyError, AttributeError):
            return super().get_authenticators()

    """
    Usage:
    authentication_classes = [] # default
    authentication_classes_action = {
        'list': []
    }
    """


class PermissionMixin:
    permission_action_classes = {}

    def get_permissions(self):
        try:
            permission_classes = self.permission_action_classes[self.action]
            return [permission() for permission in permission_classes]
        except (KeyError, AttributeError):
            return super().get_permissions()

    """
    Usage:
    permission_classes = [] # default
    permission_action_classes = {
        'list': []
    }
    """

class BaseGenericViewSet(GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_action_classes = {}
    serializer_method_classes = None
    serializer_action_classes = None
    serializer_class = NoneSerializer

    filter_backends = [DjangoFilterBackend]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = None

    def get_permissions(self):
        try:
            permission_classes = self.permission_action_classes[self.action]
            return [permission() for permission in permission_classes]
        except (KeyError, AttributeError):
            return super().get_permissions()

    def get_serializer_class(self):
        try:
            if self.serializer_method_classes is not None:
                return self.serializer_method_classes[self.request.method]
            if self.serializer_action_classes is not None:
                return self.serializer_action_classes[self.action]

            return self.serializer_class
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def finalize_response(self, request, response, *args, **kwargs):
        if not response.exception:
            response.data = BaseResponse(data=response.data).data

        return super().finalize_response(request, response, args, kwargs)


class BaseModelViewSet(BaseGenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin):
    pass
