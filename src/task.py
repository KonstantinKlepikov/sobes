import random
import threading
import time
from typing import Dict, List, Tuple


def generate_thumbnail(data: bytes) -> bytes:
    """Resize image to fit a thumbnail size"""
    print(str(data))
    return data


class Connect:
    """This is an interface; you can't change it."""

    def __init__(self):
        self.id = random.randint(0, 100000)

    def is_ready(self) -> bool:
        """Checks if connect is ready to read or write"""
        time.sleep(0.5)
        print(f'{self.id} ready')
        return random.choice([True, False])

    def read(self) -> bytes:
        """Waits until ready then reads data"""
        print(f'{self.id} read')
        return b'12234567890'

    def write(self, data: bytes):
        """Waits until ready then writes data"""
        print(f'{self.id} write')


def process(connects: List[Connect]):
    for connect in connects:
        image = connect.read()
        thumbnail = generate_thumbnail(image)
        connect.write(thumbnail)


"""
1. generate_thumbnail она задействует cpu
2. если is_ready true, то тогда мы готовы писать/читать
3. для каждого Connect мы читаем, затем трансформируем, затем пишем

Решение:

1. получать все соединения согласовано -> можем прочитать согласовано
2. затем (2) мы можем обработать изображения в отдельных процессах, если их много
3. затем согласованно записать
4. хорошо было бы это сделать как-то по мере поступления данных

Что будем делать:

- [x] попробуем получить все соединения согалсованно
- [x] читать данные
"""


def async_read(results: List[bytes], connect: Connect) -> None:
    """
    FIXME: мы не уверены что он будет вообще когда-нибудь готов
    """
    while not connect.is_ready():
        continue

    results[id(connect)] = connect.read()


def read_data(connects: List[Connect]) -> Tuple[Dict[int, Connect], Dict[int, bytes]]:
    """
    FIXME: ждем весь результат чтения сразу
    """

    conn_map: Dict[int, Connect] = {}
    results: Dict[int, bytes] = {}
    thrs: List[threading.Thread] = []

    for connect in connects:
        conn_map[id(connect)] = connect
        thr = threading.Thread(target=async_read, args=(results, connect))
        thrs.append(thr)
        thr.start()

    for thr in thrs:
        thr.join()

    return conn_map, results


def transform_data(raw_files: Dict[int, bytes]) -> Dict[int, bytes]:
    """"""

    # мы должны создать пул процессов
    # должны создать безопасную структуру, в которую мы будем сохранять результат
    # должны вернуть этот результат

    return {k: generate_thumbnail(v) for k, v in raw_files.items()}


def write_data(conn_map: Dict[int, Connect], data_map: Dict[int, bytes]) -> None:
    """ """
    thrs: List[threading.Thread] = []
    for k, v in data_map.items():
        connect = conn_map[k]
        thr = threading.Thread(target=connect.write, args=(v,))
        thrs.append(thr)
        thr.start()

    for thr in thrs:
        thr.join()


if __name__ == '__main__':

    connects = [Connect() for _ in range(5)]
    conn_map, raw_files = read_data(connects)
    transformed_files = transform_data(raw_files)
    write_data(conn_map, transformed_files)
