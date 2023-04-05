from datetime import datetime, timedelta

from jwt import ExpiredSignatureError, DecodeError

from apps.account.models import User
from apps.common.jwt_handle import jwt_encode_handler, jwt_decode_handler
from apps.common.custom_exception_handler import CustomAPIException


def generate_token_register_email(user):
    payload = {
        'id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=1),
    }
    return jwt_encode_handler(payload)


def validate_token_verify_email(token):
    try:
        payload = jwt_decode_handler(token)
    except ExpiredSignatureError as e:
        raise CustomAPIException('Token verify email expired!') from e
    except DecodeError as e:
        raise CustomAPIException('Invalid Token!') from e
    except Exception as e:
        raise CustomAPIException('Invalid token.') from e

    try:
        user = User.objects.get(pk=payload.get(
            'id'), email=payload.get('email'))
    except User.DoesNotExist as exc:
        raise CustomAPIException('Invalid token.') from exc

    return user
