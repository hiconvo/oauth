import os
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from .templates import templates
from .handlers import email_form, email


async def not_found(request, exc):
    return templates.TemplateResponse("404.html", {"request": request}, exc.status_code)


async def server_error(request, exc):
    return templates.TemplateResponse("500.html", {"request": request}, exc.status_code)


app = Starlette(
    debug=os.getenv("DEBUG", False),
    routes=[
        Route("/", email_form, methods=["GET"]),
        Route("/email", email, methods=["POST"]),
        Mount("/", app=StaticFiles(directory="static")),
    ],
    exception_handlers={404: not_found, 500: server_error},
)
