import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import os
from django.conf import settings
from django.utils import six


def _get_setting(name):
    setting_name = "DEFF_{}".format(name)
    return os.getenv(setting_name, getattr(settings, setting_name, None))


def get_bytes(v):

    if isinstance(v, six.string_types):
        return bytes(v.encode("utf-8"))

    if isinstance(v, bytes):
        return v

    raise TypeError(
        "SALT & PASSWORD must be specified as strings that convert nicely to "
        "bytes."
    )


SALT = get_bytes(_get_setting("SALT"))
PASSWORD = get_bytes(_get_setting("PASSWORD"))

class Cryptographer(object):

    _fernet = Fernet(base64.urlsafe_b64encode(PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
        backend=default_backend()
    ).derive(PASSWORD)))

    @classmethod
    def encrypted(cls, content):
        return cls._fernet.encrypt(content)

    @classmethod
    def decrypted(cls, content):
        return cls._fernet.decrypt(content)