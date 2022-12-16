import random
from datetime import datetime

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.encoding import force_bytes
from django.utils.http import base36_to_int, urlsafe_base64_encode, urlsafe_base64_decode

from apps.auth.jwt.models import ResetPasswordReferent
from apps.common.jwt_handle import jwt_encode_handler, jwt_decode_handler


class CustomEmailVerifyTokenGenerator:
    RESET_PASSWORD_CODE_LENGTH = 6
    RESET_PASSWORD_CODE_EXPIRATION_TIME = 60

    def make_token(self, user, time_token):
        return jwt_encode_handler(
            {
                'user_reset_password': user.id,
                'orig_iat': time_token
            }
        )

    def check_token(self, token):
        try:
            payload = jwt_decode_handler(token)
        except Exception:
            return False, None
        user_id = payload.get('user_reset_password')
        reset_pass_ref = ResetPasswordReferent.objects.filter(
            user_id=user_id,
            token=payload.get('orig_iat'),
            is_active=True
        ).first()
        if not reset_pass_ref:
            return False, None
        return True, reset_pass_ref.user_id

    def make_code(self, user, time_token):
        token_length = settings.RESET_PASSWORD_CODE_LENGTH or self.RESET_PASSWORD_CODE_LENGTH
        allowed_chars = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        code = "".join(random.sample(allowed_chars, token_length))
        ResetPasswordReferent.objects.filter(user_id=user).delete()
        ResetPasswordReferent.objects.create(user_id=user, code=code, token=time_token)
        return code

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
    key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"
    algorithm = None
    secret = settings.SECRET_KEY

    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return str(user.pk) + user.password + str(login_timestamp) + str(timestamp)

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
        return urlsafe_base64_encode(force_bytes(user.pk))

    def decode_uid(self, uid):
        try:
            return urlsafe_base64_decode(uid).decode()
        except:
            return None
