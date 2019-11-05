# -*- encoding: utf-8 -*-

import json
import signal
import six
import time
import uuid

from datetime import datetime
from requests import Response
from requests.adapters import BaseAdapter
from requests.hooks import dispatch_hook
from kombu import Connection, BrokerConnection
from kombu.pools import connections

from rca.url_parser import Parser, LegacyParser
from rca.exceptions import FirstConnectionTimeout

def build_response(request, data, code, encoding):
    response = Response()

    response.encoding = encoding

    # Fill in some useful fields.

    raw = six.BytesIO()
    raw.write(data)
    raw.seek(0)

    response.raw = raw
    response.url = request.url
    response.request = request
    response.status_code = code

    # Run the response hook.
    response = dispatch_hook('response', request.hooks, response)
    return response


class CeleryAdapter(BaseAdapter):
    def __init__(self, *args, **kwargs):
        self.first_connection_timeout = kwargs.pop('first_connection_timeout', None)
        super(CeleryAdapter, self).__init__(*args, **kwargs)

    @staticmethod
    def __get_parsed_url(request):
        #  backward compatibility check to support version 1.0.0 API
        #  This should be removed at some time.
        if 'task' in request.headers:
            return LegacyParser(request)
        return Parser(request.url)

    def _timeout_handler(self, signum, frame):
        raise FirstConnectionTimeout("First Connection to Broker has timed out.")

    def send(self, request, **kwargs):
        parsed_url = self.__get_parsed_url(request)
        connection = Connection(parsed_url.broker_url)
        with connections[connection].acquire(block=True) as conn:
            return self._send(conn, request, parsed_url, **kwargs)

    def _send(self, conn, request, parsed_url, **kwargs):

        # Setup an alarm timeout if first_connection_timeout is set
        previous_handler = None
        if self.first_connection_timeout:
            previous_handler = signal.signal(signal.SIGALRM, self._timeout_handler)
            signal.alarm(self.first_connection_timeout)
            self.first_connection_timeout = None

        simple_queue = conn.SimpleQueue(
            parsed_url.queue
        )

        # If alarm was set, remove it and set original handler
        if previous_handler is not None:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous_handler)


        message = {
            "id": uuid.uuid4().hex,
            "task": parsed_url.task,
            "args": [],
            "kwargs": json.loads(
                request.body if isinstance(
                    request.body, str) else request.body.decode('utf-8')
            ),
        }

        simple_queue.put(message)
        simple_queue.close()

        data = six.b(json.dumps({}))

        return build_response(request, data, 200, 'ascii')


class AmqpCeleryAdapter(CeleryAdapter):
    pass


class SQSCeleryAdapter(CeleryAdapter):
    def send(self, request, **kwargs):
        parsed_url = self.__get_parsed_url(request)
        with BrokerConnection(parsed_url.broker_url, transport_options={'region': 'sa-east-1'}) as conn:
            return self._send(conn, request, parsed_url, **kwargs)


class RedisCeleryAdapter(CeleryAdapter):
    pass
