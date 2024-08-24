from contextlib import contextmanager
import requests

class Error(Exception):
    pass

class InvalidGoldenKey(Error):
    """
    Исключение для некорректного golden_key.
    """
    def __init__(self):
        pass

    def __str__(self):
        return "An invalid golden_key is specified, double-check the golden_key and try again"
    
class NoTextToMedia(Error):
    """
    Исключение для попытки отправить текст с медиа-файлом.
    """
    def __str__(self):
        return "You cannot send text along with a media file"

class NoTextToMedia(Error):
    """
    Исключение для попытки отправить текст с медиа-файлом.
    """
    def __str__(self):
        return "You cannot send text along with a media file"
    
class ReviewError(Error):
    """
    Исключение для ошибки при работе с отзывом.
    """
    def __init__(self, response: requests.Response, error: str | None, order_id: str):
        super(ReviewError, self).__init__(response)
        self.error = error
        self.order_id = order_id
        if not self.error:
            self.log_response = True

    def short_str(self):
        return f"Ошибка при работе с отзывом: {self.order_id}" \
               f"{f': {self.error_message}' if self.error_message else '.'}"

class RefundError(Error):
    """
    Исключение для ошибки при возврате средств.
    """
    def __init__(self, response: requests.Response, error: str | None, order_id: str):
        super(RefundError, self).__init__(response)
        self.error = error
        self.order_id = order_id
        if not self.error:
            self.log_response = True

    def short_str(self):
        return f"Ошибка при возврате средств: {self.order_id}" \
               f"{f': {self.error}' if self.error else '.'}"
    
@contextmanager
def suppress(*exceptions):
    """
    Контекстный менеджер для игнорирования исключений.
    """
    try:
        yield
    except exceptions:
        pass
