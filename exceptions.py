"""Module for exceptions"""
from typing import Any, Dict, Optional


class BaseInteractionError(Exception):
    default_message = 'Backend interaction error'

    def __init__(self, *, service, method, message=None):
        self.message = message or self.default_message
        self.service = service
        self.method = method

    @property
    def name(self):
        return self.__class__.__name__

    def __str__(self):
        return f'{self.__class__.__name__}({self.service}, {self.method}): {self.message}'


class InteractionResponseError(BaseInteractionError):
    default_message = 'Backend unexpected response'

    def __init__(
            self, *,
            status_code: int,
            method: str,
            service: str,
            message: Optional[str] = None,
            response_status: Optional[str] = None,
            params: Optional[Dict[str, Any]] = None,
    ):
        """
        :param status_code: HTTP status code
        :param method: HTTP method
        :param response_status: статус ответа, который обычно приходит в JSON-теле ответа
            в ключе "status", например:
            >>> {"status": "failure", ... }
            >>> {"status": "success", ... }
        :param service: имя сервиса (просто строчка с человекочитаемым названием сервиса, в который делается запрос)
        :param params: какие-то структурированные параметры из тела ответа с ошибкой
        :param message: строка с сообщение об ошибке. в свободной форме
        """
        self.status_code = status_code
        self.response_status = response_status
        self.params = params
        super().__init__(service=service, method=method, message=message)

    def __str__(self):
        return (f'{self.__class__.__name__}({self.service}.{self.method}): '
                f'status={self.status_code} response_status={self.response_status} '
                f'params={self.params} {self.message}')


class TransactionValueError(BaseInteractionError):
    pass
