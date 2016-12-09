from django.conf import settings
import string
from math import floor

alphabet = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ_abcdefghijkmnopqrstuvwxyz'


def encode(url_id):
    return numtosxgf(url_id, settings.SHORT_URL_MAX_LEN)


def decode(code):
    return sxgtonum(code)


# http://faruk.akgul.org/blog/tantek-celiks-newbase60-in-python-and-java/
# encode number to base60
def numtosxg(n):
    s = ''
    char_list = alphabet
    if not isinstance(n, (int,)) or n == 0:
        return '0'
    while n > 0:
        n, i = divmod(n, 60)
        s = char_list[i] + s
    return s


# number to base60, padding chars (string length)
def numtosxgf(n, f):
    s = numtosxg(n)
    if not isinstance(f, (int,)):
        f = 1
    f -= len(s)
    while f > 0:
        s = '0' + s
        f -= 1
    return s


# convert string to number base60
def sxgtonum(s):
    n = 0
    j = len(s)
    for i in range(0, j):
        c = ord(s[i])
        if 48 <= c <= 57:
            c -= 48
        elif 65 <= c <= 72:
            c -= 55
        elif c == 73 or c == 108:  # typo capital I, lowercase l to 1
            c = 1
        elif 74 <= c <= 78:
            c -= 56
        elif c == 79:  # error correct typo capital O to 0
            c = 0
        elif 80 <= c <= 90:
            c -= 57
        elif c == 95:
            c = 34
        elif 97 <= c <= 107:
            c -= 62
        elif 109 <= c <= 122:
            c -= 63
        else:
            c = 0  # treat all other noise as 0
        n = 60 * n + c

    return n


def to_base62(num, b=62):
    if b <= 0 or b > 62:
        return 0
    base = string.digits + string.ascii_letters
    r = num % b
    res = base[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res


def to_base10(num, b=62):
    base = string.digits + string.ascii_letters
    limit = len(num)
    res = 0
    for i in range(limit):
        res = b * res + base.find(num[i])
    return res
