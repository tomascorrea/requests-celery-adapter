#!/usr/bin/env python

import json
import click
import requests
from rca.adapters import AmqpCeleryAdapter


@click.command()
@click.argument('url')
@click.argument('task')
@click.argument('queue')
def send_task(url, task, queue):

    s = requests.Session()
    s.mount('amqp://', AmqpCeleryAdapter())

    headers = {'task': task, 'queue': queue}

    s.post(url, headers=headers, data=json.dumps({'ola': 'ola'}))


if __name__ == '__main__':
    send_task()
