# coding=utf-8

import random
import string

def randomwords(length):
    random.seed()
    return ''.join(random.choice(string.ascii_lowercase 
                + string.ascii_uppercase + string.digits) for i in range(length))
