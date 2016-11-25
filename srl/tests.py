from django.test import TestCase

from srl.services.parse import numtosxg, sxgtonum
from srl.management.commands.create_fake_users import create_fake_users
from srl.views import get_random_user
from django.contrib.auth.models import User

class TestBaseConversion(TestCase):
    def test_check0(self):
        assert numtosxg(0) == '0'

    def test_check1(self):
        assert numtosxg(1) == '1'

    def test_check60(self):
        assert numtosxg(60) == '10'


class TestBaseConversionReverse(TestCase):
    def test_check0(self):
        assert sxgtonum('0') == 0

    def test_check1(self):
        assert sxgtonum('1') == 1

    def test_check60(self):
        assert sxgtonum('10') == 60

    def test_check1337(self):
        assert sxgtonum('NH') == 1337

    def test_checkl(self):
        assert sxgtonum('l') == 1

    def test_checkI(self):
        assert sxgtonum('I') == 1

    def test_checkO(self):
        assert sxgtonum('O') == 0

    def test_checkpipe(self):
        assert sxgtonum('|') == 0

    def test_checkcomma(self):
        assert sxgtonum(',') == 0


class TestRoundtripCheck(TestCase):
    def test_roundtrip(self):
        #  sxgtonum(numtosxg(n))==n for all n
        for integer in range(0, 6000):
            sxg = numtosxg(integer)
            result = sxgtonum(sxg)
            assert integer == result


class TestRandomUser(TestCase):
    def test_get_random_user(self):
        create_fake_users(10)
        u = get_random_user()
        assert isinstance(u, User)