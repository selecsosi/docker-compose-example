import json
import os
from time import sleep

from .celery import app


@app.task
def do_work():
    print("I'm doing some async work")
    sleep(5)
    print("Finished my async work")


def do_work_async():
    return do_work.delay()
