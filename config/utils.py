import hashlib
import time


def get_sha512(p0):
    return hashlib.sha3_512(p0.encode('utf-8')).hexdigest()


def get_token(p0):
    return get_sha512(p0 + ':' + (time.time() * 1000).__int__().__str__())


