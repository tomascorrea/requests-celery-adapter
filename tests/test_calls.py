# -*- coding: utf-8 -*-
import mock
import requests as _requests

from rca.adapters import RedisCeleryAdapter

requests = _requests.Session()
requests.mount('redis://', RedisCeleryAdapter())


class TestRemoteCalls(object):
    @mock.patch("rca.adapters.connections")
    def test_remote_call(self, rca_adapters_connections):
        url = 'redis://broker-production.test.cache.amazonaws.com:6379/1/api.v1.loan.soft_deny#geru.loan'
        resp = requests.post(url=url, json={})
        assert resp.ok == True
