import datetime
import os
from threading import Lock

import configs.log_config as cfg

"""
Класс для ведения лога. Может писать как в файл, так и в консоль (куда писать указывается в файле
log_config.py, возможно одновременно и туда, и туда)
Имя файла для печати: log.log . Файл создаётся в родительской дирректории.

У лога есть три уровня:
N - Normal  - Обычное сообщение
W - Warning - Сообщение, повышенной важности, на которое нужно обратить внимание
E - Error   - Сообщение об ошибке

Чтобы написать лог, нужно вызывать метод src.log.n, src.log.e или src.log.w (зависит от уровня
важности лога). Первый параметр тег, второй сообщение. В качестве тега рекомендуется создать
отдельную переменную в модуле скрипта (либо как приватную переменную у класса), которая равна
названию файла скрипта (без .py) либо название класса. Если это уникальный объект, уникальный идентификатор 
добавляется к стандартному тегу через @. 
Например:
tag = "data_models"
tag = "M3u8Watcher@camera_name"

Пример вызова:
        import src.log as log
        tag = "main"
        log.n(tag, "Hello world!")
и выводимое сообщение о логе будет выглядеть следующим образом
        14:21:20.875531 N main: Hello world!
    
Структура выводимого сообщения:
[ВРЕМЯ] [ВАЖНОСТЬ] [ТЕГ]: [СООБЩЕНИЕ]
Внимание! Дата в строчке не пишется.
"""

__print_lock__ = Lock()


def n(tag, msg):
    """ Выводит в лог нормальное сообщение, без сообщений об ошибке и без важны предупреждений """
    timestamp = datetime.datetime.now().time()
    logline = str(timestamp) + " N " + tag + ": " + msg
    if cfg.print_to_console:
        __print_to_console__(logline)
    if cfg.print_to_file:
        __print_to_file__(logline)


def w(tag, msg):
    """ Выводит в лог сообщение повышенной важности, на которое нужно обратить внимание """
    timestamp = datetime.datetime.now().time()
    logline = str(timestamp) + " W " + tag + ": " + msg
    if cfg.print_to_console:
        __print_to_console__(logline)
    if cfg.print_to_file:
        __print_to_file__(logline)


def e(tag, msg):
    """ Выводит в лог сообщение об ошибке """
    timestamp = datetime.datetime.now().time()
    logline = str(timestamp) + " E " + tag + ": " + msg
    if cfg.print_to_console:
        __print_to_console__(logline)
    if cfg.print_to_file:
        __print_to_file__(logline)


#
# Конец публичной зоны
#

def __init__():
    if not cfg.print_to_console and not cfg.print_to_file:
        logline = str(
            datetime.datetime.now().time()) + " W " + "log.py" + ": " + "Вывод лога отключён и в файл, и в консоль"
        __print_to_console__(logline)


def __print_to_console__(logline):
    with __print_lock__:
        print(logline)


def __print_to_file__(logline):
    path_parent = os.path.abspath(os.getcwd())
    path = os.path.join(path_parent, "log.log")
    with __print_lock__:
        with open(path, 'a') as f:
            f.write(logline + "\n")
