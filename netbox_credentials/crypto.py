"""
Symmetric encryption helpers using Fernet.
The encryption key is derived from Django's SECRET_KEY so there is nothing
extra to configure.
"""

import base64
import hashlib

from cryptography.fernet import Fernet
from django.conf import settings


def _get_fernet() -> Fernet:
    """Derive a 32-byte Fernet key from SECRET_KEY."""
    digest = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    key = base64.urlsafe_b64encode(digest)
    return Fernet(key)


def encrypt(plaintext: str) -> str:
    """Encrypt a plaintext string → base64 token stored in the DB."""
    if not plaintext:
        return ""
    return _get_fernet().encrypt(plaintext.encode()).decode()


def decrypt(token: str) -> str:
    """Decrypt a stored token back to plaintext."""
    if not token:
        return ""
    return _get_fernet().decrypt(token.encode()).decode()
