from urllib.parse import quote, urlencode

import pyotp

from apps.totp.models import UserOtpDevice


class TotpService:
    def __init__(self, algorithm='SHA1', digits=6, step=30):
        self.algorithm = algorithm
        self.digits = digits
        self.step = step

    def provisioning_uri(self, user_id):
        instance, is_create = self._get_or_create_totp_user(user_id=user_id)
        return self._generate_uri(user_totp=instance)

    def verify(self, user_id, otp):
        instance = UserOtpDevice.objects.filter(user_id=user_id).first()
        if not instance:
            return False

        totp = pyotp.TOTP(instance.key)
        if not totp.verify(otp):
            return False

        return True

    def _get_label_name(self, user):
        return user.username

    def _get_or_create_totp_user(self, user_id):
        secret = pyotp.random_base32()
        instance, is_create = UserOtpDevice.objects.get_or_create(user_id=user_id, defaults={'key': secret})
        return instance, is_create

    def _generate_uri(self, user_totp):
        label = self._get_label_name(user_totp.user)
        params = {
            'secret': user_totp.key,
            'algorithm': self.algorithm,
            'digits': self.digits,
            'period': self.step,
        }
        urlencoded_params = urlencode(params)

        uri = 'otpauth://totp/{}?{}'.format(quote(label), urlencoded_params)
        return uri
