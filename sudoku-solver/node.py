import sys
import json


def ready():
    emit({
        'status': 'ready'
    })

def end():
    emit({
        'status': 'end'
    })


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def recive():
    incoming = input()
    return json.loads(incoming)


def emit(data):
    print(json.dumps(data))
