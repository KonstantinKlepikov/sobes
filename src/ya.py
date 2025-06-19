"""
Нам нужно передать данные из некоторого источника некоторому потребителю.
При этом источник отдает данные небольшими пачками (~ десятки записей),
а потребитель оптимальнее работает с крупными батчами (~тысячи записей).
Реальный пример - поставка данных из очередей типа Kafka в базу Clickhouse.

Источник:
- Условно бесконечный.
- Источник никогда не возвращает более max_items записей за один вызов next.
- В рамках одной "сессии" (одного вызова функции pipe) источник каждый раз возвращает
новые данные на каждый вызов next.
- Однако, после перезапуска источник начнет с прошлой "подтвержденной" позиции,
задаваемой cookie.
    Поэтому *каждое* значение cookie, которое вернул вызов next, после сохранения
    данных в приемнике,
    должно быть фиксировано вызовом commit, причем строго в той же последовательности,
    в которой их вернул next

Приемник:
- Не может обработать более max_items за один раз.

Требуется реализовать функцию pipe(self, producer: Producer, consumer: Consumer)
которая читает данные из источника, группирует их в буфер размером не более max_items
и сохраняет в приёмник,
после чего фиксирует прогресс в источнике.
"""

import dataclasses
from typing import Any, TypeAlias

Cookie: TypeAlias = int


@dataclasses.dataclass
class Result:
    """Однако, после перезапуска источник начнет с прошлой "подтвержденной" позиции,
    задаваемой cookie"""

    items: list[Any]
    cookie: Cookie


class ProducerException(Exception):
    """
    An exception is thrown when the producer
    is unable to produce data or commit a cookie.
    """


class ConsumerException(Exception):
    """
    An exception is thrown when the consumer is unable to consume data any further.
    """


class Producer:
    """
    This is an interface; you can't change it.
    """

    def next(self) -> Result:   # type: ignore
        """Источник никогда не возвращает более max_items записей за один вызов next"""
        ...

    def commit(self, cookie: Cookie) -> None:
        """*каждое* значение cookie, которое вернул вызов next, после сохранения
        данных в приемнике,
        должно быть фиксировано вызовом commit,
        причем строго в той же последовательности,
        в которой их вернул next"""
        ...


class Consumer:
    """
    This is an interface; you can't change it.
    """

    max_items: int = 1000

    def process(self, items: list[Any]) -> None:
        ...


class PipeProcessor:
    """
    1. запрашивать продюсер в цикле по next
    2. полученный резалт складывать в некую структуру, причем порядок, должен быть
    гарантирован, так как ожидается, что мы будем сообщать что отправили далее
    3. нужно передавать не более max_items - делать это в цикле,
    если мы накопили сколько-то (?)
    4. нужно коммитить, когда мы сделали отправку тем куки, который мы отправили

    """

    def __init__(self):
        ...

    def pipe(self, producer: Producer, consumer: Consumer) -> None:
        """"""
        items: list[Result] = []

        while True:

            income = producer.next()
            howmuch = 0
            # TODO:  избавиться от опрсоа длины в цикле внутир while
            # наивное решение - счетчик над while
            for i in items:
                howmuch += len(i.items)

            howmuch += len(income.items)

            for_send = []
            if howmuch > consumer.max_items:
                # TODO: избавиться от обхода списка в цикле, сделать
                # сделать pop(), придется сохранить адишники для вызова в commit
                for i in items:
                    for j in i.items:
                        for_send.append(j)

                consumer.process(for_send)

                for i in items:
                    producer.commit(i.cookie)

                items.clear()

            items.append(income)
