import functools
import urllib
import httpx
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException

from .templates import templates
from .csrf import csrf_signer


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
            }
            return await func(request, context)

        return inject_context

    return wrapped


@with_context("email")
async def email_form(request, context):
    return templates.TemplateResponse("email_form.html", context)


@with_context("email")
async def email(request, context):
    form = await request.form()
    form_data = dict(form)

    if not csrf_signer.validate(form_data["csrf"], max_age=120):
        context["error"] = "Whoops! Please try again."
        return templates.TemplateResponse("email_form.html", context, 400)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.hiconvo.com/users/auth",
            json={
                "email": form_data.get("email", ""),
                "password": form_data.get("password", ""),
            },
        )

    if response.status_code >= 500:
        context["error"] = "Whoops! Please try again."
        return templates.TemplateResponse("email_form.html", context, 400)

    json = response.json()

    if response.status_code != 200:
        context["error"] = json.get("message", "Invalid credentials.")
        return templates.TemplateResponse("email_form.html", context, 400)

    token = json.get("token")
    redirect_uri = context.get("unquoted_redirect_uri")

    return RedirectResponse(
        url=f"{redirect_uri}?token={urllib.parse.quote(token)}", status_code=302
    )
