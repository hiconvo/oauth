import functools
import urllib
import httpx
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException

from .templates import templates
from .csrf import csrf_signer
from .env import GOOGLE_API_KEY, GOOGLE_CLIENT_ID, FACEBOOK_APP_ID


def with_context(action):
    def wrapped(func):
        @functools.wraps(func)
        async def inject_context(request):
            redirect_uri = request.query_params.get("redirect_uri")
            if not redirect_uri:
                raise HTTPException(404)
            quoted_redirect_uri = urllib.parse.quote(redirect_uri)
            context = {
                "request": request,
                "csrf": csrf_signer.sign("").decode("utf-8"),
                "action": f"/{action}?redirect_uri={quoted_redirect_uri}",
                "redirect_uri": quoted_redirect_uri,
                "unquoted_redirect_uri": redirect_uri,
                "google_api_key": GOOGLE_API_KEY,
                "google_client_id": GOOGLE_CLIENT_ID,
                "facebook_app_id": FACEBOOK_APP_ID,
            }
            return await func(request, context)

        return inject_context

    return wrapped


def with_form_handling(template):
    def wrapped(func):
        @functools.wraps(func)
        async def handle_form(request, context):
            form = await request.form()
            form_data = dict(form)

            if not csrf_signer.validate(form_data["csrf"], max_age=120):
                context["error"] = "Whoops! Please try again."
                return templates.TemplateResponse(template, context, 400)

            response = await func(request, context, form_data)

            if response.status_code >= 500:
                context["error"] = "Whoops! Please try again."
                return templates.TemplateResponse(template, context, 400)

            json = response.json()

            if response.status_code != 200:
                context["error"] = json.get("message", "Invalid credentials.")
                return templates.TemplateResponse(template, context, 400)

            token = json.get("token")
            redirect_uri = context.get("unquoted_redirect_uri")

            return RedirectResponse(
                url=f"{redirect_uri}?token={token}", status_code=302
            )

        return handle_form

    return wrapped


@with_context("oauth")
async def oauth_form(request, context):
    return templates.TemplateResponse("oauth_form.html", context)


@with_context("oauth")
@with_form_handling("oauth_form.html")
async def oauth(request, context, form_data):
    async with httpx.AsyncClient() as client:
        return await client.post(
            "https://api.hiconvo.com/users/oauth",
            json={
                "provider": form_data.get("provider", ""),
                "token": form_data.get("token", ""),
            },
        )


@with_context("email")
async def email_form(request, context):
    return templates.TemplateResponse("email_form.html", context)


@with_context("email")
@with_form_handling("email_form.html")
async def email(request, context, form_data):
    async with httpx.AsyncClient() as client:
        return await client.post(
            "https://api.hiconvo.com/users/auth",
            json={
                "email": form_data.get("email", ""),
                "password": form_data.get("password", ""),
            },
        )
