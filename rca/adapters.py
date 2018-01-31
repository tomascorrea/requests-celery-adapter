# -*- encoding: utf-8 -*-

import uuid
import json
from requests import Response
from requests.adapters import BaseAdapter
from requests.hooks import dispatch_hook
from kombu import Connection, BrokerConnection
from kombu.pools import connections
import datetime
import six

from rca.url_parser import Parser, LegacyParser


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
    @staticmethod
    def __get_parsed_url(request):
        #  backward compatibility check to support version 1.0.0 API
        #  This should be removed at some time.
        if 'task' in request.headers:
            return LegacyParser(request)
        return Parser(request.url)

    def send(self, request, **kwargs):
        parsed_url = self.__get_parsed_url(request)
        connection = Connection(parsed_url.broker_url)
        with connections[connection].acquire(block=True) as conn:
            return self._send(conn, request, parsed_url, **kwargs)

    def _send(self, conn, request, parsed_url, **kwargs):

        simple_queue = conn.SimpleQueue(
            parsed_url.queue
        )

        message = {"id": uuid.uuid4().hex,
                   "task": parsed_url.task,
                   "args": [],
                   "kwargs": json.loads(
                       request.body if isinstance(request.body, str) else request.body.decode('utf-8')
                   ),
                   "eta": datetime.datetime.now().isoformat()}

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




