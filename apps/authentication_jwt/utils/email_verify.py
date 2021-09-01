import random
from datetime import datetime
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import base36_to_int
from django.utils.crypto import constant_time_compare

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


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):

    def make_token(self, user):
        return self._make_token_with_timestamp(user, self._num_seconds(self._now()))

    def check_token(self, user, token):
        if not (user and token):
            return False
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False
        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            if not constant_time_compare(
                    self._make_token_with_timestamp(user, ts, legacy=True),
                    token,
            ):
                return False

        # Check the timestamp is within limit.
        if (self._num_seconds(self._now()) - ts) > settings.RESET_PASSWORD_EXPIRATION_TIME:
            return False

        return True

    def make_uid(self, user):
        return 1

    def decode_uid(self, uid):
        return 1
