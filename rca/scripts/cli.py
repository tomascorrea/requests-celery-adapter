#!/usr/bin/env python

import json
import click
import requests
from rca.adapters import AmqpCeleryAdapter, SQSCeleryAdapter, RedisCeleryAdapter


@click.command()
@click.argument('url')
@click.argument('task')
@click.argument('queue')
@click.option('--params')
def send_task(url, task, queue, params):

    s = requests.Session()
    s.mount('amqp://', AmqpCeleryAdapter())
    s.mount('sqs://', SQSCeleryAdapter())
    s.mount('redis://', RedisCeleryAdapter())

    headers = {'task': task, 'queue': queue}

    if params:
        params = json.dumps(json.loads(params))
    else:
        params = json.dumps({})

    s.post(url, headers=headers, data=params)


if __name__ == '__main__':
    send_task()
