import base64

import requests

from apps.paypal.config import paypal_settings


class PayPalService:
    SANDBOX_API_URL = 'https://api.sandbox.paypal.com'
    SANDBOX_WEB_URL = 'https://www.sandbox.paypal.com'

    LIVE_API_URL = 'https://api.paypal.com'
    LIVE_WEB_URL = 'https://www.paypal.com'

    BASE_API_URL = SANDBOX_API_URL
    BASE_WEB_URL = SANDBOX_WEB_URL

    def __int__(self):
        if paypal_settings.PAYPAL_ENV == 'live':
            self.BASE_API_URL = self.LIVE_API_URL
            self.BASE_WEB_URL = self.LIVE_WEB_URL

    def get_paypal_token(self, client_id, client_secret):
        url = f"{self.BASE_API_URL}/v1/oauth2/token"
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {0}".format(
                base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
            ),
        }

        token = requests.post(url, data, headers=headers)
        return token.json()['access_token']

    def create_order(self, purchase_units):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_paypal_token(paypal_settings.CLIENT_ID, paypal_settings.CLIENT_SECRET)}',
        }
        json_data = {
            "intent": "CAPTURE",
            "purchase_units": purchase_units
        }
        url = f"{self.BASE_API_URL}/v2/checkout/orders"
        return requests.post(url, headers=headers, json=json_data)

    def capture_order(self, order_id):
        url = f"{self.BASE_API_URL}/v2/checkout/orders/{order_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.get_paypal_token(paypal_settings.CLIENT_ID, paypal_settings.CLIENT_SECRET)}",
        }
        return requests.post(url, headers=headers)
