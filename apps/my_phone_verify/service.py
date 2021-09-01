import random
from datetime import datetime

import requests
from django.core.exceptions import ImproperlyConfigured

from Example import settings
from apps.authentication_jwt.utils.jwt_handle import jwt_encode_handler
from apps.my_phone_verify.models import Phone


class PhoneVerificationService:
    try:
        phone_settings = settings.PHONE_VERIFICATION
    except AttributeError:
        raise ImproperlyConfigured("Please define PHONE_VERIFICATION in settings")

    from_phone = phone_settings.get('OPTIONS').get('FROM')
    sid_phone = phone_settings.get('OPTIONS').get('SID')
    secret_phone = phone_settings.get('OPTIONS').get('SECRET')
    DEFAULT_TOKEN_LENGTH = 6
    SECURITY_CODE_EXPIRATION_TIME = phone_settings.get('SECURITY_CODE_EXPIRATION_TIME')

    SECURITY_CODE_VALID = 0
    SECURITY_CODE_INVALID = 1
    SECURITY_CODE_EXPIRED = 2
    SECURITY_CODE_VERIFIED = 3
    SESSION_TOKEN_INVALID = 4

    def send_security_code(self, message, to):
        url = 'https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json'.format(self.sid_phone)
        data = {'To': to, 'From': self.from_phone, 'Body': message}
        auth = (self.sid_phone, self.secret_phone)
        res = requests.post(url=url, data=data, auth=auth)
        return res

    def generate_security_code(self):
        """
        Returns a unique random `security_code` for given `TOKEN_LENGTH` in the settings.
        """
        token_length = settings.PHONE_VERIFICATION.get(
            "TOKEN_LENGTH", self.DEFAULT_TOKEN_LENGTH
        )
        allowed_chars = '0123456789'
        return "".join(random.sample(allowed_chars, token_length))

    def generate_session_token(self, phone_number):
        payload = {
            'phone_number': phone_number,
        }
        return jwt_encode_handler(payload)

    def validate_security_code(self, security_code, phone_number, session_token):
        phone = Phone.objects.filter(security_code=security_code, phone_number=phone_number).first()
        if phone is None:
            return self.SECURITY_CODE_INVALID

        if phone.session_token != session_token:
            return self.SESSION_TOKEN_INVALID

        if (datetime.now().astimezone() - phone.created_at).seconds > self.SECURITY_CODE_EXPIRATION_TIME:
            return self.SECURITY_CODE_EXPIRED

        if phone.is_verified:
            return self.SECURITY_CODE_VERIFIED

        phone.is_verified = True
        phone.save()
        return self.SECURITY_CODE_VALID
