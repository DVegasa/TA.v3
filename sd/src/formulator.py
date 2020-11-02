from abc import ABC, abstractmethod

from multiprocessing.queues import Queue


class M3u8Formulator(ABC):
    """
    Абстрактный класс, для связки различно форматированных m3u8, и остальной программы.
    Каждому сервису, кто поставляет m3u8, нужно создать свой формулятор, потому что
    в разных сервисах описание .ts сегментов может отличаться.
    """
    queue: Queue = None
    m3u8_url: str = None
    ts_base_url: str = None

    @abstractmethod
    def update_queue(self):
        """Скачивает m3u8 файл, просматривает его и если появились новые TS сегменты,
           добавляет их в очередь. В очереди не должно быть повторяющихся элементов"""
        pass
