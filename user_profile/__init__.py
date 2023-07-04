import random
import string
from uuid import uuid4


def get_random_code(length=6):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_random_token():
    return uuid4()