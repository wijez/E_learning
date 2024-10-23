import random
import string


def generate_verification_code(length=6):
    """Hàm sinh mã xác thực ngẫu nhiên gồm chữ cái và chữ số."""
    characters = string.ascii_letters + string.digits  # Bao gồm chữ cái và số
    verification_code = ''.join(random.choice(characters) for _ in range(length))
    return verification_code
