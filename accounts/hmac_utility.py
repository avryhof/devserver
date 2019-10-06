import base64
import datetime
import hashlib
import hmac
from urllib.parse import quote_plus

from django.conf import settings


class HMACUtility:
    api_key = None
    api_secret = None
    salt = None
    encoded_salt = None

    is_debug = False
    show_encode = False

    def __init__(self, api_key, api_secret=False, **kwargs):
        self.api_key = api_key

        if not api_secret:
            self.api_secret = settings.SECRET_KEY
        else:
            self.api_secret = api_secret

        self.is_debug = kwargs.get("debug", False)
        self.show_encode = kwargs.get("show_encode", False)

        if kwargs.get("salt"):
            in_salt = kwargs.get("salt")
            self.salt = str(in_salt)

        else:
            self.salt = self.timestamp_as_millis()

        self.encode_salt()

    def debug_msg(self, message):
        if self.is_debug:
            print(message)

    def get_bytes(self, value):
        retn = value.encode("utf8")

        return retn

    def base64encode(self, value):
        base64_value = base64.b64encode(value)
        return_value = quote_plus(base64_value)

        if self.show_encode:
            self.debug_msg("Input Value")
            self.debug_msg(value)
            self.debug_msg("Base64 Value")
            self.debug_msg(base64_value)
            self.debug_msg("URLencoded Base64 Value")
            self.debug_msg(return_value)

        return return_value

    def timestamp_as_millis(self, **kwargs):
        if not kwargs.get("fake"):
            now = datetime.datetime.utcnow()
            epoch = datetime.datetime.utcfromtimestamp(0)

            self.salt = str(int((now - epoch).total_seconds() * 1000))
            if self.show_encode:
                self.debug_msg("SALT: %s" % self.salt)

        return self.salt

    def encode_salt(self):
        if not isinstance(self.salt, str):
            self.salt = str(self.salt)

        try:
            if self.show_encode:
                self.debug_msg("ENCODING SALT:")
            self.encoded_salt = self.base64encode(self.salt)

        except Exception as e:
            self.debug_msg("ERROR: %s" % e)

        return self.encoded_salt

    def generate_hmac(self):
        algo = hashlib.sha256

        secret_key = self.get_bytes(self.api_secret)
        salted_api_key = self.api_key + self.salt

        salted_key_bytes = self.get_bytes(salted_api_key)

        raw_hmac = hmac.new(secret_key, salted_key_bytes, digestmod=algo).digest()

        encoded_hmac = self.base64encode(raw_hmac)

        return encoded_hmac
