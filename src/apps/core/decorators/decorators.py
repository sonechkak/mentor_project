import logging
from functools import wraps


def decode_request_body(request) -> str:
    try:
        if hasattr(request, "data"):
            return request.data
        return request.body.decode("utf-8") if request.body else None
    except UnicodeDecodeError:
        return "Не удалось декодировать тело запроса"
    except Exception as e:
        return f"Ошибка при обработке тела запроса: {e}"


def log_request_operations(logger_name):
    """
    Декоратор для логирования.
    :param logger_name: Имя логгера для записи сообщений.
    :return:
    """
    logger = logging.getLogger(logger_name)

    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            user_ip = request.META.get("REMOTE_ADDR")
            user = request.user
            path = request.path
            method = request.method

            query_params = (
                request.query_params.dict()
                if hasattr(request, "query_params")
                else request.GET.dict()
            )
            body = decode_request_body(request=request)

            common_text = (
                f" Метод {method} на {path}"
                f" Пользователь: {user} с IP {user_ip}"
                f" query_params: {query_params}, body: {body}"
            )

            try:
                result = func(self, request, *args, **kwargs)
                logger.info(f"Успех: {common_text}")
                return result
            except Exception as e:
                logger.exception(f"Ошибка: {common_text}, Причина: {e}")
                raise

        return wrapper

    return decorator
