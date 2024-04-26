import abc
import httpx


class ResultsObserver(abc.ABC):
    @abc.abstractmethod
    def observe(self, data: bytes) -> None: ...


async def do_reliable_request(url: str,
                              observer: ResultsObserver,
                              timeout=10.0) -> None:
    """
    Одна из главных проблем распределённых систем - это ненадёжность связи.

    Ваша задача заключается в том, чтобы таким образом исправить этот код,
    чтобы он умел переживать возвраты ошибок и таймауты со стороны сервера,
    гарантируя успешный запрос (в реальной жизни такая гарантия невозможна,
    но мы чуть упростим себе задачу).

    Все успешно полученные результаты должны регистрироваться с помощью
    обсёрвера.
    """

    async with httpx.AsyncClient() as client:
        # в реальности добавил бы кол-во попыток
        response = await client.get(url, timeout=timeout)
        while response.status_code != 200:
            response = await client.get(url, timeout=timeout)
        data = response.read()

        observer.observe(data)
        return
