import datetime
from queue import Queue
import src.log as log
import os

__q__ = Queue()


def add_to_queue(path):
    log.n("detection_queue.py", "Добавил в очередь: " + path)
    __q__.put(path)


def tracking():
    while True:
        if not __q__.empty():
            path = __q__.get()
            log.n("detection_queue.py", "Начал детектить: " + path)
            os.system('cmd /c '
                      + 'python object_tracker.py --model yolov4 '
                        '--video ' + path + ' '
                        '--output ' + path + '.avi ')
