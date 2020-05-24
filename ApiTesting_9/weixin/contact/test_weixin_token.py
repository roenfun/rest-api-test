# from unittest import TestCase

from weixin.contact.weixin_token import Weixin
import pytest


# class TestWeixin(TestCase):
class TestWeixin(object):
    def test_get_token(self):
        w_token = Weixin.get_token()
        print(w_token)
        assert w_token != ""
