import os

from app.models import User_ConfirmationHash


def generate_unique_hash(type):
    h = ''
    while True:
        h = os.urandom(16).encode('hex')
        is_free = User_ConfirmationHash.objects.filter(type = type, hash = h).count() == 0
        if is_free:
            break
    return h