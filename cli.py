#!/usr/bin/env python

import json
import click
import requests
from rca.adapters import AmqpCeleryAdapter, SQSCeleryAdapter


@click.command()
@click.argument('url')
@click.argument('task')
@click.argument('queue')
@click.argument('adapter')
@click.option('--params')
def send_task(url, task, queue, params, adapter):

    s = requests.Session()
    if adapter == 'ampq':
        s.mount('amqp://', AmqpCeleryAdapter())
    elif adapter == 'sqs':
        s.mount('sqs://', SQSCeleryAdapter())

    headers = {'task': task, 'queue': queue}

    if params:
        params = json.dumps(json.loads(params))
    else:
        params = json.dumps({})

    s.post(url, headers=headers, data=params)


if __name__ == '__main__':
    send_task()
