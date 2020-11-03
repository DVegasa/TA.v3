import datetime


class TsSegment:
    """
    Представляет мета-данные о ts сегменте, полученным из m3u8 файла
    """

    TYPE_TS_CONTENT = 1
    TYPE_TS_AD = 2

    def __init__(self, uri, duration, start_time, type_):
        self.uri = uri  # Абсолютная ссылка на скачивание сегмента
        self.duration: float = duration  # В секундах. Допустимы не целые значения
        self.start_time: datetime.datetime = start_time
        self.type: int = type_

    @property
    def end_time(self):
        return self.start_time + datetime.timedelta(milliseconds=self.duration * 100)

    def str_short(self) -> str:
        """
        Возвращает короткое имя сегмента. Цифры означают минуты-секунды из параметра 'start_time'
        """
        return "TS-" + self.start_time.strftime("%M%S")

    def __str__(self):
        """
        Возвращает полную информацию о всех полях (кроме ссылки) о данном сегменте
        """
        if self.type == self.TYPE_TS_AD:
            return "[TsSegment]: Ad"
        else:
            return "[TsSegment]: {} (duration {} sec)".format(self.start_time, self.duration)
