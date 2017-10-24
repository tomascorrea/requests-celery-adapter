# -*- coding: utf-8 -*-
import mock
from rca.url_parser import Parser, LegacyParser


class TestTaskUrlParser(object):
    def test_url_parser_redis(self):
        url = 'redis://broker-production.test.cache.amazonaws.com:6379/1/api.v1.loan.soft_deny#geru.loan'
        parser = Parser(url)
        assert parser.queue == 'geru.loan'
        assert parser.task == 'api.v1.loan.soft_deny'
        assert parser.broker_url == 'redis://broker-production.test.cache.amazonaws.com:6379/1'

    def test_url_parser_rabbitmq_vhost(self):
        url = 'amqp://myuser:mypassword@localhost:5672/myvhost/api.v1.loan.soft_deny#geru.loan'
        parser = Parser(url)
        assert parser.queue == 'geru.loan'
        assert parser.task == 'api.v1.loan.soft_deny'
        assert parser.broker_url == 'amqp://myuser:mypassword@localhost:5672/myvhost'

    def test_url_parser_rabbitmq_no_vhost(self):
        url = 'amqp://myuser:mypassword@localhost:5672/api.v1.loan.soft_deny#geru.loan'
        parser = Parser(url)
        assert parser.queue == 'geru.loan'
        assert parser.task == 'api.v1.loan.soft_deny'
        assert parser.broker_url == 'amqp://myuser:mypassword@localhost:5672'

    def test_url_parser_sqs_with_credentials(self):
        url = 'sqs://ABCDEFGHIJKLMNOPQRST:ZYXK7NiynGlTogH8Nj+P9nlE73sq3@/api.v1.loan.soft_deny#geru.loan'
        parser = Parser(url)
        assert parser.queue == 'geru.loan'
        assert parser.task == 'api.v1.loan.soft_deny'
        assert parser.broker_url == 'sqs://ABCDEFGHIJKLMNOPQRST:ZYXK7NiynGlTogH8Nj+P9nlE73sq3@'

    def test_url_parser_sqs_without_credentials(self):
        url = 'sqs:///api.v1.loan.soft_deny#geru.loan'
        parser = Parser(url)
        assert parser.queue == 'geru.loan'
        assert parser.task == 'api.v1.loan.soft_deny'
        assert parser.broker_url == 'sqs://'


class TestTaskUrlLegacyParser(object):
    @staticmethod
    def _request(url, headers):
        request = mock.Mock()
        request.url = url
        request.headers =headers
        return request

    def test_url_parser_redis(self):
        url = 'redis://broker-production.test.cache.amazonaws.com:6379/1'
        headers = {
            'task': 'api.v1.loan.soft_deny',
            'queue': 'geru.loan'
        }
        parser = LegacyParser(self._request(url, headers))
        assert parser.queue == 'geru.loan'
        assert parser.task == 'api.v1.loan.soft_deny'
        assert parser.broker_url == 'redis://broker-production.test.cache.amazonaws.com:6379/1'

    def test_url_parser_rabbitmq_vhost(self):
        url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
        headers = {
            'task': 'api.v1.loan.soft_deny',
            'queue': 'geru.loan'
        }
        parser = LegacyParser(self._request(url, headers))
        assert parser.queue == 'geru.loan'
        assert parser.task == 'api.v1.loan.soft_deny'
        assert parser.broker_url == 'amqp://myuser:mypassword@localhost:5672/myvhost'

    def test_url_parser_rabbitmq_no_vhost(self):
        url = 'amqp://myuser:mypassword@localhost:5672'
        headers = {
            'task': 'api.v1.loan.soft_deny',
            'queue': 'geru.loan'
        }
        parser = LegacyParser(self._request(url, headers))
        assert parser.queue == 'geru.loan'
        assert parser.task == 'api.v1.loan.soft_deny'
        assert parser.broker_url == 'amqp://myuser:mypassword@localhost:5672'

    def test_url_parser_sqs_with_credentials(self):
        url = 'sqs://ABCDEFGHIJKLMNOPQRST:ZYXK7NiynGlTogH8Nj+P9nlE73sq3@'
        headers = {
            'task': 'api.v1.loan.soft_deny',
            'queue': 'geru.loan'
        }
        parser = LegacyParser(self._request(url, headers))
        assert parser.queue == 'geru.loan'
        assert parser.task == 'api.v1.loan.soft_deny'
        assert parser.broker_url == 'sqs://ABCDEFGHIJKLMNOPQRST:ZYXK7NiynGlTogH8Nj+P9nlE73sq3@'

    def test_url_parser_sqs_without_credentials(self):
        url = 'sqs://'
        headers = {
            'task': 'api.v1.loan.soft_deny',
            'queue': 'geru.loan'
        }
        parser = LegacyParser(self._request(url, headers))
        assert parser.queue == 'geru.loan'
        assert parser.task == 'api.v1.loan.soft_deny'
        assert parser.broker_url == 'sqs://'
