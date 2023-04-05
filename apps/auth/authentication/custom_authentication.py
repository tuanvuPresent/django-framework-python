import datetime
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from Example.settings import EXPIRING_TOKEN_DURATION


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise NotAuthenticated()

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError as e:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise AuthenticationFailed(msg) from e

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist as e:
            raise AuthenticationFailed() from e

        if is_expired(token):
            raise AuthenticationFailed('Token has expired')

        return token.user, token


def is_expired(token):
    return timezone.now() - token.created - EXPIRING_TOKEN_DURATION > datetime.timedelta(seconds=0)
