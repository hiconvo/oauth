import os
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from .handlers import oauth_form, oauth, email_form, email


app = Starlette(
    debug=os.getenv("DEBUG"),
    routes=[
        Route("/", oauth_form, methods=["GET"]),
        Route("/oauth", oauth, methods=["POST"]),
        Route("/email", email_form, methods=["GET"]),
        Route("/email", email, methods=["POST"]),
        Mount("/", app=StaticFiles(directory="static")),
    ],
)
