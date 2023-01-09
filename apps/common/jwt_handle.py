from datetime import datetime
import uuid
import jwt
from rest_framework_jwt.settings import api_settings


def jwt_encode_handler(payload):
    return jwt.encode(
        payload,
        api_settings.JWT_SECRET_KEY,
        api_settings.JWT_ALGORITHM
    ).decode('utf-8')


def jwt_decode_handler(token):
    return jwt.decode(
        token,
        api_settings.JWT_SECRET_KEY,
        algorithms=[api_settings.JWT_ALGORITHM]
    )


class JwtTokenGenerator:

    def get_token(self, user):
        payload = self.set_payload(user)
        return jwt.encode(
            payload,
            self.secret_key,
            api_settings.JWT_ALGORITHM
        ).decode('utf-8')

    def verify_token(self, token):
        self.payload = jwt.decode(
            token,
            self.secret_key,
            algorithms=[api_settings.JWT_ALGORITHM]
        )
        return self.payload

    def set_payload(self, user):
        self.payload = {}
        self.payload['user_id'] = user.pk
        self.payload['username'] = user.username
        self.payload['exp'] = datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        self.payload['jti'] = uuid.uuid4()
        self.payload['iat'] = datetime.now().timestamp()
        return self.payload

    @property
    def secret_key(self):
        return str(api_settings.JWT_SECRET_KEY)

    @property
    def user_id(self):
        return self.payload.get('user_id')

    @property
    def username(self):
        return self.payload.get('username')

    @property
    def exp(self):
        return self.payload.get('exp')

    @property
    def iat(self):
        return self.payload.get('iat')


class RefreshJwtTokenGenerator(JwtTokenGenerator):
    def verify_refresh_token(self, token):
        self.payload = jwt.decode(
            token,
            self.secret_key,
            algorithms=[api_settings.JWT_ALGORITHM]
        )
        self._validate_refresh_token_exp()
        return self.payload

    def _validate_refresh_token_exp(self):
        orig_iat = self.iat
        if api_settings.JWT_ALLOW_REFRESH:
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA.total_seconds()

            expiration_timestamp = orig_iat + int(refresh_limit)
            now_timestamp = datetime.now().astimezone().timestamp()
            if now_timestamp > expiration_timestamp:
                raise CustomAPIException('Refresh has expired.')
        else:
            raise CustomAPIException('Not allow refresh.')
