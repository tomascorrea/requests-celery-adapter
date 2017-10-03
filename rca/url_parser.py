# -*- coding: utf-8 -*-
import six
import posixpath


class LegacyParser(object):
    def __init__(self, request):
        self.request = request

    @property
    def queue(self):
        return self.request.headers.get('queue', 'default')

    @property
    def task(self):
        return self.request.headers['task']

    @property
    def broker_url(self):
        return self.request.url


class Parser(object):
    def __init__(self, url):
        """

        :param url: formated url
         -> Format: <scheme>://<broker url>/<task_name>#queue
            e.g: redis://myredis.example.com/process_request#process_queue
        """
        self._parsed = six.moves.urllib.parse.urlparse(url)
        self._broker_path, self._task = self._path_split()
        self._queue = self._parsed.fragment

    def _path_split(self):
        broker_path, task = posixpath.split(self._parsed.path)
        broker_path = broker_path[1:] if broker_path.startswith(posixpath.sep) else broker_path
        return broker_path, task

    @property
    def queue(self):
        return self._queue

    @property
    def task(self):
        return self._task

    @property
    def broker_url(self):
        # Avoid posixpath.join from append '/' at the end if self._broker_path is an empty string.
        _endpoint = posixpath.join(self._parsed.netloc, self._broker_path) if self._broker_path else self._parsed.netloc
        return "{}://{}".format(self._parsed.scheme, _endpoint)
