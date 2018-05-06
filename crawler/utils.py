# -*- coding: utf-8 -*-

import hashlib

def md5(string, encoding = 'utf-8'):
    return hashlib.md5(bytes(string, encoding = encoding)).hexdigest()
