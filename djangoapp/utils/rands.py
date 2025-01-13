import string
from random import SystemRandom

from django.utils.text import slugify

def random_letters(k):
    return ''.join(SystemRandom.choices(SystemRandom(),
        population=string.ascii_letters+string.digits,
        k=k
    ))
    
def slugify_new(text, k=5):
    return slugify(text) + '-' + random_letters(k)
    