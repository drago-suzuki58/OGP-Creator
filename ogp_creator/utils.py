import random
import string

import ogp_creator.env as env

def generate_random_path() -> str:
    while True:
        path = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if path not in env.RESERVED_PATHS:
            return path
