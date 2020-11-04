import datetime
import os
import time
from queue import Queue

import requests

import src.file_manager as files
import src.formulator
import src.log as log
from src.data_models import TsSegment
import src.detection_queue

class M3u8Watcher:
    """
    Класс, который будет наблюдать за отдельно взятым m3u8, используя M3u8Formulator из этого файла
    будут браться .ts файлы и компоноваться в один большой, с помощью методов grabber.

    Флаг '_d' в конце названия файла uTS (но до расширения .ts) указывает на то, что данный uTS не является
    неразрывным продолжением предыдущего uTS, то есть межу данным и предыдущим uTS есть разрыв видео. Данный
    флаг должен учитываться модулем распознавания машин, чтобы не делать связывание машин с двух подряд идущих
    uTS видео.
    """

    class Config:
        """
        Вспомогательный класс для M3u8Formulator, поставляющий настройки для отдельно взятого объекта.
        Все параметры обязательны, однако некоторые определены стандартными значениями.
        """
        m3u8_url = None  # Ссылка на объект m3u8

        m3u8_update_delay = 4  # Задержка между обновлением m3u8 файла в секундах, допустимы дробные значения

        ts_base_url = None  # Если ts в m3u8 заданы относительно, то Formulator будет использовать эту ссылку
        # как базовую. Если абсолютно, оставьте поле пустым, но не None

        name = None  # Имя потока. Должно быть уникально. Используется в логах, файловой системе и других аспектах.

        uTS_duration = 60  # Минимальное время uTS, к которому будет стремиться итоговый uTS сверху.
        # Итоговая длительность uTS не обязательно будет равна этому значению, но точно будет
        # не меньше этого значения.

        tolerance = 0.04  # Допустимая погрешность к uTS_duration. Рекомендуется не изменять, так как длительность
        # отдельных .ts может колебаться в районе 0.01 секунды, что влияет на uTS

        output_path = os.path.join(os.path.abspath(os.getcwd()), "data_storage", "uTS")
        # Папка, куда будут записываться записи.
        # Дополнительно для каждого M3u8Watcher будет создана подпапка

        formulator: src.formulator.M3u8Formulator = None  # Класс наследние от M3u8Formulator, используемый для
        # обработки m3u8 файла

        timezone_h_fix = 0  # Если камера возвращает дату в другом часовом поясе, изменение этого параметра исправит

        # значение часа на верное, прибавив данное число к данным полученным от камеры. Например, если камера работает
        # в часовом поясе UTC0, то установив данный параметр равным 4, время на записи будет в зоне UTC+4

        def isValid(self) -> bool:
            """
            Проверяет составленный конфиг на корректность
            """
            result = True

            tag = "M3u8Watcher.Config@" + self.non_null_name()

            if self.m3u8_url is None:
                result = False
                log.e(tag, "Не указан обязательный параметр m3u8_url")

            if self.non_null_name() == "$noname":
                result = False
                log.e(tag, "Не указан обязательный параметр name")

            if self.ts_base_url is None:
                result = False
                log.e(tag, "Не указан обязательный параметр ts_base_url")

            if self.output_path is None:
                result = False
                log.e(tag, "Не указан обязательный параметр output_path")

            if not self.m3u8_update_delay > 0:
                result = False
                log.e(tag, "Значение m3u8_update_delay отрицательное. Необходимо положительное.")

            if self.m3u8_update_delay < 1:
                log.w(tag, "Значение m3u8_update_delay менее одной секунды (" + str(self.m3u8_update_delay) + "мс)")

            if not self.uTS_duration > 0:
                result = False
                log.e(tag, "Значение max_duration_combined отрицательное. Необходимо положительное.")

            if self.formulator is None:
                result = False
                log.e(tag, "Не назначен M3u8Formulator")

            return result

        def non_null_name(self):
            """
            Возвращает "$noname" если 'name' равно None, иначе возвращает значения поля 'name'
            Так как при работе программы имя не может быть None,
            этот метод вызывается следует вызывать на этапе валидации данных.
            """
            if self.name is not None:
                return self.name
            else:
                return "$noname"

    def __init__(self, config: Config):
        self.isReadyToUse = False  # Готов ли этот M3u8Watcher к запуску
        self.tag = "M3u8Watcher@" + config.non_null_name()
        if config.isValid():
            self.__config__ = config
            log.n(self.tag, "Поток настроен успешно и готов к использованию")
            self.isReadyToUse = True
        else:
            log.e(self.tag, "Конфиг настроен неправильно. Поток не будет подключён")
            self.isReadyToUse = False

        # Локальные переменные
        self.__q__ = Queue()
        self.__ts_buffer_duration__ = 0
        self.__cur_ts_file_name__ = None
        self.__start_is_discontinuity__ = True

    def start(self):
        """
        Запускает работу M3u8Watcher, начинается скачивание трансляции.
        """
        if not self.isReadyToUse:
            log.e(self.tag, "Конфиг настроен неправильно. Старт потока невозможен")
            return
        # Связываем формулятор с нашей очередью
        self.__config__.formulator.queue = self.__q__
        log.n(self.tag, "Старт потока")
        self.__running_code__()

    #
    # Конец публичной зоны
    #

    def __running_code__(self):
        while True:
            start_time = datetime.datetime.now()

            # region Hard work
            self.__config__.formulator.update_queue()
            self.__grabber__()
            # endregion Hard work

            # Перезапуск через интервальное время
            cur_time = datetime.datetime.now()
            work_time = (cur_time - start_time).total_seconds()
            delay = self.__config__.m3u8_update_delay - work_time
            if delay < 0:
                log.w(self.tag, "Performance issue! Выполнения потока заняло {:.3f}x от update_delay".format(
                    work_time / self.__config__.m3u8_update_delay) + " ({:.3f} сек)".format(work_time))
                delay = 0
            time.sleep(delay)

    # formulator составляет очередь из объектов TsSegment, которые нужно скачать. Ответственнен за
    # правильную последовательность сегментов в очереди. Если последовательный неразрывный порядок
    # нельзя соблюсти (например, рекламный участок видео), вставляет в очередь TsSegment типа TYPE_TS_AD
    #
    # grabber скачивает из очереди эти сегменты и поочерёдно соединяет их в единый файл. Если в очереди оказался
    # TYPE_TS_AD, "закрывает" текущий буфер, сохраняет его. Последующие сегменты сохраняются в новый файл, а также
    # этот новый файл получит флаг '_d' указывающий на разрыв с предыдущим uTS.

    def __grabber__(self):
        while self.__q__.qsize() != 0:
            ts_seg = self.__q__.get()
            if ts_seg.type is TsSegment.TYPE_TS_CONTENT:
                ts_content = self.__download_ts_content__(ts_seg)
            else:
                ts_content = None
            self.__append_ts_content__(ts_seg, ts_content)

    def __download_ts_content__(self, ts_seg):
        r = requests.get(ts_seg.uri)
        return r.content

    def __append_ts_content__(self, ts_seg: TsSegment, ts_content):
        camera_path = os.path.join(self.__config__.output_path, str(self.__config__.non_null_name()))

        if not os.path.exists(camera_path):
            os.makedirs(camera_path)

        if ts_seg.type == TsSegment.TYPE_TS_CONTENT:
            if self.__cur_ts_file_name__ is None:  # Файл дозаписи ещё не создан
                # Нужно сгенерировать имя этого файла, чтобы туда можно было дозаписывать
                self.__cur_ts_file_name__ = self.__generate_full_uTS_file_name__(ts_seg)

            # Дозаписываем в файл - добавлем в mp.Queue а file_manager в едином потоке по очереди всё записывает в
            # соотвествующие файлы
            files.append_queue.put((os.path.join(camera_path, str(self.__cur_ts_file_name__)), ts_content))
            self.__ts_buffer_duration__ += ts_seg.duration
            log.n(self.tag, "Буфер дополнен. Новая длительность буфера: "
                  + "{:.3f}".format(self.__ts_buffer_duration__)
                  + " сек")

            # Проверяем на длительность uTS
            if self.__ts_buffer_duration__ + self.__config__.tolerance >= self.__config__.uTS_duration:
                # Если uTS достаточно длинный, закрываем этот файл
                self.__close_file__()

        elif ts_seg.type == TsSegment.TYPE_TS_AD:
            if self.__cur_ts_file_name__ is None:  # Файл дозаписи ещё не создан
                log.n(self.tag, "Получен рекламный сегмент, но файл дозаписи ещё не создан. Действия не требуются")
                return  # Ничего делать не нужно
            else:  # Файл открыт на дозапись
                log.w(self.tag, "Получен рекламный сегмент, текущий uTS будет закрыт, "
                                "дальнейшее видео запишется в новый uTS")
                self.__close_file__()  # Закрываем этот файл, писать будем в новый
                self.__start_is_discontinuity__ = True

    def __close_file__(self):
        log.n(self.tag, "uTS закрыт: " + self.__cur_ts_file_name__ + " ("
              + "{:.3f}".format(self.__ts_buffer_duration__)
              + " сек)")

        self.__start_tracking__(self.__config__.name, self.__cur_ts_file_name__)

        self.__cur_ts_file_name__ = None
        self.__ts_buffer_duration__ = 0

    def __start_tracking__(self, cam_name, video_name):
        path = './data_storage/uTS/' + cam_name + '/' + video_name
        src.detection_queue.add_to_queue(path)
        # os.system('cmd /c '
        #           + 'python object_tracker.py --model yolov4 '
        #             '--video ' + path + ' '
        #             '--output ' + path + '.avi ')

    def __generate_full_uTS_file_name__(self, ts_segment) -> str:
        # uTS_200814_T10:00:00.ts
        name = ts_segment.start_time.strftime("uTS_" + self.__config__.name + "_%y%m%d_T%H%M%S")

        # Если данный uTS не является неразрывным продолжением предыдущего,
        # то в его названии в конце добавляется флаг '_d'
        if self.__start_is_discontinuity__:
            name = "d_" + name + ".ts"
            self.__start_is_discontinuity__ = False
        else:
            name += ".ts"
        return name
