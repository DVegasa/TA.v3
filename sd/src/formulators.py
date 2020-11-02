import datetime

import m3u8

import src.formulator
import src.stream_receiving
from src.data_models import TsSegment


class PowernetFormulator(src.formulator.M3u8Formulator):

    def __init__(self, config: src.stream_receiving.M3u8Watcher.Config):
        self.m3u8_url = config.m3u8_url
        self.ts_base_url = config.ts_base_url
        self.name = config.non_null_name()
        self.tag = "PowernetFormulator@" + str(self.name)
        self.timezone_fix = config.timezone_h_fix

    __ad_met__ = False

    def update_queue(self):
        playlist = m3u8.load(self.m3u8_url)
        for s in playlist.segments:
            try:
                start_time = self.__parse_time__(s.uri)
                dur = s.duration
                uri = self.ts_base_url + str(s.uri)
                ts_segment = TsSegment(
                    uri=uri,
                    duration=dur,
                    start_time=start_time,
                    type_=TsSegment.TYPE_TS_CONTENT
                )
                self.__add_if_needed__(ts_segment)

            except ValueError:
                # Эта ветка сработает, если Powernet отправил рекламный ts
                ts_segment = TsSegment(
                    uri=None,
                    duration=0,
                    start_time=None,
                    type_=TsSegment.TYPE_TS_AD
                )

                # Если реклама встречается только единожды, при первом подключении, то эта условная ветка будет работать
                # корректно -- добавлять только первое упоминание рекламного сегмента, а остальные игнорировать.
                # Если же реклама может встретиться ещё когда-то, помимо первого подключения, то данный условный блок
                # нужно будет переработать
                if not self.__ad_met__:
                    self.queue.put(ts_segment)
                    self.__ad_met__ = True

    #
    # Конец публичной зоны
    #

    __last_start_time__ = None
    __tolerance__ = 0.08

    def __add_if_needed__(self, ts_segment):
        if self.__last_start_time__ is None \
                or ts_segment.start_time > self.__last_start_time__:
            self.queue.put(ts_segment)
            self.__last_start_time__ = ts_segment.end_time

    # Пример относительного пути, из которого нужно вытащить данные о дате и времени записи
    # "2020/02/27/07/45/12-06000.ts?token=f0f5fdcf-dce2-4f91-bca0-fd2dd1c3af60"
    def __parse_time__(self, uri):
        y = int(uri[0:4])
        m = int(uri[5:7])
        d = int(uri[8:10])
        h = int(uri[11:13]) + self.timezone_fix
        minutes = int(uri[14:16])
        s = int(uri[17:19])
        ms = int(uri[20:25])
        start_time = datetime.datetime(y, m, d, h, minutes, s, ms)
        return start_time
