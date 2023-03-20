from typing import Callable


# Меняем ASGI-приложение, поставляемой Django-ой, на своё.
# В нём мы получаем scope, а в scope - path,
# а на основе path можем выбрать, какому приложению давать работать:
# от Django или от FastAPI
async def application(scope: dict, receive: Callable, send: Callable) -> None:
    if scope["type"] != "http" or not scope["path"].startswith("/api"):
        import os

        from django.core.asgi import get_asgi_application

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
        asgi_django = get_asgi_application()
        return await asgi_django(scope, receive, send)

    else:
        from api.app import app as asgi_fastapi

        return await asgi_fastapi(scope, receive, send)
