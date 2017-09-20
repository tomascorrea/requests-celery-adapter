# -*- coding: utf-8 -*-
import six
import posixpath


"""
    core_broker_url = redis://broker-production.erdvhn.0001.sae1.cache.amazonaws.com:6379/1
    queue = geru.loan

    headers = {'task': 'api.v1.loan.soft_deny', 'queue': queue}

    data = {
        'loan_uuid': loan_uuid,
        'score': geru_score,
        'rate': operation_rate,
        'interest': interest,
        'capacity': capacity['monthly_supported_value'],
        'new_principal': new_principal,
        'new_instalment_number': length
    }

    requests.post(
        core_broker_url, headers=headers,
        data=json.dumps(data)
    )


    redis://broker-production.erdvhn.0001.sae1.cache.amazonaws.com:6379/1/api.v1.loan.soft_deny/geru.loan


"""


class Parser(object):
    def __init__(self, url):
        self._parsed = six.moves.urllib.parse.urlparse(url)
        self._broker_path, self._task, self._queue = self._path_split()

    def _path_split(self):
        path, queue = posixpath.split(self._parsed.path)
        broker_path, task = posixpath.split(path)
        broker_path = broker_path[1:] if broker_path.startswith(posixpath.sep) else broker_path
        return broker_path, task, queue

    @property
    def queue(self):
        return self._queue

    @property
    def task(self):
        return self._task

    @property
    def broker_url(self):
        # Avoids posixpath.join from append '/' at the end if self._broker_path is an empty string.
        _endpoint = posixpath.join(self._parsed.netloc, self._broker_path) if self._broker_path else self._parsed.netloc
        return "{}://{}".format(self._parsed.scheme, _endpoint)
