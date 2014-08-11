# -*- encoding: utf-8 -*-

import uuid
import json
from requests import Response
from requests.compat import urlparse, StringIO
from requests.adapters import BaseAdapter
from requests.hooks import dispatch_hook
from kombu import Connection, Exchange, Queue, BrokerConnection
import datetime


def build_response(request, data, code, encoding):
    response = Response()

    response.encoding = encoding

    # Fill in some useful fields.

    raw = StringIO()
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

    def send(self, request, **kwargs):

        with Connection(request.url) as conn:
            return self._send(conn, request, **kwargs)


    def _send(self, conn, request, **kwargs):

        simple_queue = conn.SimpleQueue(
            request.headers.get('queue', 'default')
        )

        message = {"id": uuid.uuid4().hex,
                   "task": request.headers['task'],
                   "args": [],
                   "kwargs": json.loads(request.body),
                   "retries": request.headers.get('retries', 0),
                   "eta": datetime.datetime.now().isoformat()}

        simple_queue.put(message)
        simple_queue.close()

        data = json.dumps({})

        return build_response(request, data, 200, 'ascii')



class AmqpCeleryAdapter(CeleryAdapter):
    pass

class SQSCeleryAdapter(CeleryAdapter):
    def send(self, request, **kwargs):
        with BrokerConnection(request.url, transport_options = {'region': 'sa-east-1'}) as conn:
            return self._send(conn, request, **kwargs)




