import string
import random


def code_generator(length=4):
    characters = string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code

