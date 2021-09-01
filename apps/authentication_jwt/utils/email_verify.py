import random
from datetime import datetime
from django.conf import settings
from apps.account.models import User
from apps.authentication_jwt.models import ResetPasswordReferent
from apps.authentication_jwt.utils.jwt_handle import jwt_encode_handler, jwt_decode_handler


class CustomEmailVerifyTokenGenerator:
    RESET_PASSWORD_CODE_LENGTH = 6
    RESET_PASSWORD_CODE_EXPIRATION_TIME = 60

    def make_token(self, user):
        return jwt_encode_handler(
            {
                'user_reset_password': user.id,
                'orig_iat': datetime.now().timestamp()
            }
        )

    def check_token(self, token):
        try:
            payload = jwt_decode_handler(token)
        except Exception:
            return False, None
        user_id = payload.get('user_reset_password')
        user = User.objects.filter(id=user_id).first()
        if not user:
            return False, None
        return True, user

    def make_code(self):
        token_length = settings.RESET_PASSWORD_CODE_LENGTH or self.RESET_PASSWORD_CODE_LENGTH
        allowed_chars = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return "".join(random.sample(allowed_chars, token_length))

    def check_code(self, user, code):
        reset_password_ref = ResetPasswordReferent.objects.filter(user_id=user, is_active=True).first()
        if not reset_password_ref:
            return False
        if reset_password_ref.code != code:
            return False

        code_time = settings.RESET_PASSWORD_CODE_EXPIRATION_TIME or self.RESET_PASSWORD_CODE_EXPIRATION_TIME
        if (datetime.now().astimezone() - reset_password_ref.created_at).seconds > code_time:
            return False
        reset_password_ref.is_active = False
        reset_password_ref.save()
        return True
