import hashlib
import hmac
import urllib.parse


class VNPay:
    def __init__(self):
        self.request_data = {}
        self.response_data = {}

    def get_payment_url(self, vnpay_payment_url, secret_key):
        """Build the payment URL with the provided payment URL and secret key."""
        query_string = "&".join(
            f"{key}={urllib.parse.quote_plus(str(val))}"
            for key, val in sorted(self.request_data.items())
        )
        hash_value = self.__hmac_sha512(secret_key, query_string)
        return f"{vnpay_payment_url}?{query_string}&vnp_SecureHash={hash_value}"

    def validate_response(self, secret_key):
        """Validate the response data using the provided secret key."""
        vnp_secure_hash = self.response_data.pop('vnp_SecureHash', None)
        self.response_data.pop('vnp_SecureHashType', None)

        if not vnp_secure_hash:
            return False

        hash_data = "&".join(
            f"{key}={urllib.parse.quote_plus(str(val))}"
            for key, val in sorted(self.response_data.items())
            if key.startswith('vnp_')
        )
        hash_value = self.__hmac_sha512(secret_key, hash_data)

        print(f"Validate debug, HashData: {hash_data}\nHashValue: {hash_value}\nInputHash: {vnp_secure_hash}")
        return vnp_secure_hash == hash_value

    @staticmethod
    def __hmac_sha512(key, data):
        """Generate HMAC SHA512 hash."""
        byte_key = key.encode('utf-8')
        byte_data = data.encode('utf-8')
        return hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()
